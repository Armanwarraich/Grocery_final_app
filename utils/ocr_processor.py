import os
import logging
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import AzureError, ClientAuthenticationError, ResourceNotFoundError
import re
from datetime import datetime
import streamlit as st
from typing import Optional, Dict, Any, Union
import io
from db import get_ocr_feedback, upsert_ocr_feedback  # Import your database functions

# Load environment variables if using .env
from dotenv import load_dotenv
load_dotenv()

# Configure logging for Azure operations
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AzureDocumentIntelligenceOCR:
    """
    Azure Document Intelligence OCR service following Azure best practices
    """
    
    def __init__(self):
        """Initialized the Azure Document Intelligence client with proper error handling"""
        self.endpoint = os.getenv("AZURE_DOC_INTELLIGENCE_ENDPOINT")
        self.key = os.getenv("AZURE_DOC_INTELLIGENCE_KEY")
        self.client = None
        
        if not self.endpoint or not self.key:
            logger.error("Azure Document Intelligence credentials not found")
            st.error("Azure Document Intelligence credentials not configured. Please check your environment variables.")
            return
        
        try:
            self.client = DocumentIntelligenceClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.key)
            )
            logger.info("Azure Document Intelligence client initialized successfully")
        except ClientAuthenticationError as e:
            logger.error(f"Authentication failed: {e}")
            st.error("Azure authentication failed. Please check your credentials.")
        except Exception as e:
            logger.error(f"Failed to initialize Azure client: {e}")
            st.error(f"Failed to initialize Azure service: {str(e)}")

    def extract_expiry_date(self, image_file) -> Optional[Dict[str, Any]]:
        """
        Extract expiry date and other product information from an image
        
        Args:
            image_file: Uploaded image file (from Streamlit file_uploader)
        
        Returns:
            dict: Contains extracted information including expiry_date, product_name, etc.
        """
        if not self.client:
            st.error("Azure Document Intelligence client not initialized")
            return None
            
        try:
            # Reset file pointer if needed
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            # Read the image file
            if hasattr(image_file, 'read'):
                image_bytes = image_file.read()
            else:
                image_bytes = image_file
            
            # Validate file size (Azure has limits)
            if len(image_bytes) > 50 * 1024 * 1024:  # 50MB limit
                st.error("File size too large. Please use an image smaller than 50MB.")
                return None
            
            # Analyze the document using the prebuilt-read model
            logger.info("Starting document analysis with Azure Document Intelligence")
            
            poller = self.client.begin_analyze_document(
    model_id="prebuilt-read",  # Explicit model ID
    body=image_bytes,  # Pass image bytes as 'body'
    content_type="application/octet-stream"
)

            
            # Wait for the operation to complete
            result = poller.result()
            logger.info("Document analysis completed successfully")
            
            # Extract all text content
            extracted_text = self._extract_text_from_result(result)
            
            if not extracted_text.strip():
                st.warning("No text was extracted from the image. Please try with a clearer image.")
                return None
            
            # Parse the extracted text for expiry dates and product info
            parsed_info = self._parse_product_information(extracted_text)
            
            return parsed_info
            
        except ResourceNotFoundError as e:
            logger.error(f"Azure resource not found: {e}")
            st.error("Azure Document Intelligence resource not found. Please check your endpoint.")
            return None
        except ClientAuthenticationError as e:
            logger.error(f"Authentication error: {e}")
            st.error("Authentication failed. Please check your Azure credentials.")
            return None
        except AzureError as e:
            logger.error(f"Azure service error: {e}")
            st.error(f"Azure service error: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error during OCR processing: {e}")
            st.error(f"Error during OCR processing: {str(e)}")
            return None

    def _extract_text_from_result(self, result) -> str:
        """
        Extract text from Azure Document Intelligence result
        
        Args:
            result: Azure Document Intelligence analysis result
            
        Returns:
            str: Extracted text content
        """
        extracted_text = ""
        
        if result.pages:
            for page in result.pages:
                if page.lines:
                    for line in page.lines:
                        extracted_text += line.content + "\n"
        
        return extracted_text

    def _parse_product_information(self, text: str) -> Dict[str, Any]:
        """
        Parse extracted text to find expiry dates, product names, and other relevant information
        
        Args:
            text (str): Raw text extracted from OCR
        
        Returns:
            dict: Parsed product information
        """
        result = {
            'expiry_date': None,
            'product_name': None,
            'manufacturer': None,
            'batch_number': None,
            'raw_text': text,
            'confidence': None
        }
        
        # Enhanced expiry date patterns with more variations
        expiry_patterns = [
            r'(?:exp|expiry|expires|best\s+before|use\s+by|bb|best\s+by)\s*:?\s*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(?:exp|expiry|expires|best\s+before|use\s+by|bb|best\s+by)\s*:?\s*(\d{1,2}\s+\w{3,9}\s+\d{2,4})',
            r'(?:exp|expiry|expires)\s*:?\s*(\d{1,2}\.\d{1,2}\.\d{2,4})',
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{2,4}[/-]\d{1,2}[/-]\d{1,2})',
            r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{2,4})',
            r'(\d{1,2}\.\d{1,2}\.\d{2,4})'
        ]
        
        # Search for expiry dates with priority to patterns with keywords
        for i, pattern in enumerate(expiry_patterns):
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                date_str = match.group(1)
                parsed_date = self._parse_date_string(date_str)
                if parsed_date:
                    result['expiry_date'] = parsed_date
                    result['confidence'] = 'high' if i < 3 else 'medium'  # Higher confidence for keyword-based patterns
                    break
            if result['expiry_date']:
                break
        
        # Extract product name with improved logic
        result['product_name'] = self._extract_product_name(text)
        
        # Extract manufacturer/brand
        result['manufacturer'] = self._extract_manufacturer(text)
        
        # Extract batch number
        result['batch_number'] = self._extract_batch_number(text)
        
        return result

    def _extract_product_name(self, text: str) -> Optional[str]:
        """Extract product name from text"""
        lines = text.split('\n')
        potential_names = []
        
        for i, line in enumerate(lines[:15]):  # Check first 15 lines
            line = line.strip()
            # Skip short lines, numbers, and common non-product text
            if (len(line) > 3 and 
                not re.match(r'^\d+$', line) and 
                'barcode' not in line.lower() and
                'exp' not in line.lower()[:10] and
                'mfg' not in line.lower()[:10]):
                potential_names.append((line, len(line)))
        
        # Return the longest meaningful line as product name
        if potential_names:
            return max(potential_names, key=lambda x: x[1])[0]
        return None

    def _extract_manufacturer(self, text: str) -> Optional[str]:
        """Extract manufacturer/brand from text"""
        brand_patterns = [
            r'(?:mfg|manufactured\s+by|brand|company)\s*:?\s*([a-zA-Z\s&]+)',
            r'([A-Z][a-zA-Z\s&]{3,25})\s+(?:ltd|inc|corp|pvt|limited)',
            r'(?:by\s+)([A-Z][a-zA-Z\s&]{3,25})'
        ]
        
        for pattern in brand_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _extract_batch_number(self, text: str) -> Optional[str]:
        """Extract batch number from text"""
        batch_patterns = [
            r'(?:batch|lot|b\.no|lot\s+no|batch\s+no)\s*:?\s*([a-zA-Z0-9]+)',
            r'batch\s*:?\s*([a-zA-Z0-9]+)',
            r'lot\s*:?\s*([a-zA-Z0-9]+)'
        ]
        
        for pattern in batch_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _parse_date_string(self, date_str: str) -> Optional[datetime]:
        """
        Parse various date string formats into a standardized datetime object
        
        Args:
            date_str (str): Date string to parse
        
        Returns:
            datetime or None: Parsed date object
        """
        date_formats = [
            '%d/%m/%Y', '%m/%d/%Y', '%Y/%m/%d',
            '%d-%m-%Y', '%m-%d-%Y', '%Y-%m-%d',
            '%d.%m.%Y', '%m.%d.%Y', '%Y.%m.%d',
            '%d/%m/%y', '%m/%d/%y', '%y/%m/%d',
            '%d-%m-%y', '%m-%d-%y', '%y-%m-%d',
            '%d.%m.%y', '%m.%d.%y', '%y.%m.%d',
            '%d %b %Y', '%d %B %Y',
            '%b %d %Y', '%B %d %Y',
            '%d %b %y', '%d %B %y',
            '%b %d %y', '%B %d %y'
        ]
        
        date_str = date_str.strip()
        
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                # Handle 2-digit years
                if parsed_date.year < 1950:
                    if parsed_date.year < 30:
                        parsed_date = parsed_date.replace(year=parsed_date.year + 2000)
                    else:
                        parsed_date = parsed_date.replace(year=parsed_date.year + 1900)
                return parsed_date
            except ValueError:
                continue
        
        return None

    def extract_text_only(self, image_file) -> str:
        """
        Simple text extraction without parsing - useful for debugging
        
        Args:
            image_file: Uploaded image file
        
        Returns:
            str: Raw extracted text
        """
        if not self.client:
            return "Azure Document Intelligence client not initialized"
            
        try:
            if hasattr(image_file, 'seek'):
                image_file.seek(0)
            
            image_bytes = image_file.read()
            
            poller = self.client.begin_analyze_document(
                "prebuilt-read",
                analyze_request=image_bytes,
                content_type="application/octet-stream"
            )
            
            result = poller.result()
            return self._extract_text_from_result(result)
            
        except Exception as e:
            logger.error(f"Error in text extraction: {e}")
            return f"Error: {str(e)}"

# Initialize the OCR service
ocr_service = AzureDocumentIntelligenceOCR()

# Define required functions for app compatibility
def process_image_ocr(image_path, user_email):
    """Process single image with Azure OCR"""
    with open(image_path, 'rb') as image_file:
        result = ocr_service.extract_expiry_date(image_file)
        if result:
            return result['product_name'] or "Unknown", result['expiry_date'] or "Unknown"
        return "Unknown", "Unknown"

def process_dual_image_ocr(front_image_path, back_image_path, user_email):
    """Process dual images with Azure OCR and combine results"""
    front_result = process_image_ocr(front_image_path, user_email)
    back_result = process_image_ocr(back_image_path, user_email)
    combined_product = front_result[0] if front_result[0] != "Unknown" else back_result[0]
    combined_expiry = front_result[1] if front_result[1] != "Unknown" else back_result[1]
    return combined_product, combined_expiry

def apply_hitl_feedback(user_email, image_path, pred_product, pred_expiry, user_product, user_expiry):
    """Log user corrections (implement as needed)"""
    upsert_ocr_feedback(image_path, user_email, pred_product, pred_expiry, user_product, user_expiry)
    logger.info(f"Feedback logged for user: {user_email}")

# Backward compatibility functions
def extract_expiry_date(image_file):
    return ocr_service.extract_expiry_date(image_file)

def extract_text_only(image_file):
    return ocr_service.extract_text_only(image_file)
