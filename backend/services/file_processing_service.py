"""
File processing service for PDF and image text extraction
"""

import PyPDF2
import pdfplumber
import pytesseract
from PIL import Image
import io
import os
import logging
from typing import Optional, Dict, Any
import aiofiles

logger = logging.getLogger(__name__)

class FileProcessingService:
    def __init__(self):
        """Initialize file processing service"""
        # Configure Tesseract path if needed (Windows)
        if os.name == 'nt':  # Windows
            # You may need to set the path to tesseract.exe
            # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
            pass
    
    async def extract_text_from_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Extract text from uploaded file based on type"""
        
        try:
            if file_type.lower() == 'pdf':
                return await self._extract_from_pdf(file_path)
            elif file_type.lower() in ['png', 'jpg', 'jpeg']:
                return await self._extract_from_image(file_path)
            elif file_type.lower() == 'txt':
                return await self._extract_from_text(file_path)
            elif file_type.lower() == 'docx':
                return await self._extract_from_docx(file_path)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
                
        except Exception as e:
            logger.error(f"Error extracting text from {file_type} file: {e}")
            raise Exception(f"Failed to extract text from {file_type} file: {str(e)}")
    
    async def _extract_from_pdf(self, file_path: str) -> Dict[str, Any]:
        """Extract text from PDF using multiple methods"""
        
        text_content = ""
        pages_info = []
        
        try:
            # Method 1: Using pdfplumber (better for complex layouts)
            with pdfplumber.open(file_path) as pdf:
                for page_num, page in enumerate(pdf.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
                        pages_info.append({
                            "page_number": page_num,
                            "text_length": len(page_text),
                            "has_text": True
                        })
                    else:
                        pages_info.append({
                            "page_number": page_num,
                            "text_length": 0,
                            "has_text": False
                        })
            
            # If pdfplumber didn't extract text, try PyPDF2
            if not text_content.strip():
                logger.info("pdfplumber failed, trying PyPDF2")
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page_num, page in enumerate(pdf_reader.pages, 1):
                        page_text = page.extract_text()
                        if page_text:
                            text_content += f"\n--- Page {page_num} ---\n{page_text}\n"
                            pages_info.append({
                                "page_number": page_num,
                                "text_length": len(page_text),
                                "has_text": True
                            })
            
            # If still no text, try OCR on the PDF (convert to images first)
            if not text_content.strip():
                logger.info("Text extraction failed, attempting OCR")
                text_content = await self._extract_from_pdf_with_ocr(file_path)
            
            return {
                "text": text_content.strip(),
                "extraction_method": "pdf_text_extraction",
                "pages_info": pages_info,
                "total_pages": len(pages_info),
                "success": bool(text_content.strip())
            }
            
        except Exception as e:
            logger.error(f"Error extracting from PDF: {e}")
            raise Exception(f"PDF text extraction failed: {str(e)}")
    
    async def _extract_from_pdf_with_ocr(self, file_path: str) -> str:
        """Extract text from PDF using OCR (convert PDF pages to images)"""
        
        try:
            # This is a simplified version - in production, you'd use pdf2image
            # For now, we'll return an error message
            logger.warning("OCR extraction from PDF not implemented yet")
            return "OCR extraction from PDF requires additional setup (pdf2image library)"
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    async def _extract_from_image(self, file_path: str) -> Dict[str, Any]:
        """Extract text from image using OCR"""
        
        try:
            # Open and process image
            with Image.open(file_path) as image:
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                
                # Extract text using Tesseract OCR
                text_content = pytesseract.image_to_string(image, lang='eng')
                
                # Get additional image info
                image_info = {
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode,
                    "format": image.format
                }
                
                return {
                    "text": text_content.strip(),
                    "extraction_method": "ocr",
                    "image_info": image_info,
                    "success": bool(text_content.strip())
                }
                
        except Exception as e:
            logger.error(f"Error extracting from image: {e}")
            raise Exception(f"Image OCR extraction failed: {str(e)}")
    
    async def _extract_from_text(self, file_path: str) -> Dict[str, Any]:
        """Extract text from plain text file"""
        
        try:
            async with aiofiles.open(file_path, 'r', encoding='utf-8') as file:
                text_content = await file.read()
            
            return {
                "text": text_content.strip(),
                "extraction_method": "direct_read",
                "success": bool(text_content.strip())
            }
            
        except Exception as e:
            logger.error(f"Error reading text file: {e}")
            raise Exception(f"Text file reading failed: {str(e)}")
    
    async def _extract_from_docx(self, file_path: str) -> Dict[str, Any]:
        """Extract text from DOCX file"""
        
        try:
            from docx import Document
            
            doc = Document(file_path)
            text_content = ""
            
            for paragraph in doc.paragraphs:
                text_content += paragraph.text + "\n"
            
            return {
                "text": text_content.strip(),
                "extraction_method": "docx_extraction",
                "success": bool(text_content.strip())
            }
            
        except ImportError:
            logger.error("python-docx library not installed")
            raise Exception("DOCX extraction requires python-docx library")
        except Exception as e:
            logger.error(f"Error extracting from DOCX: {e}")
            raise Exception(f"DOCX extraction failed: {str(e)}")
    
    def validate_file(self, file_path: str, file_type: str) -> Dict[str, Any]:
        """Validate uploaded file"""
        
        validation_result = {
            "valid": True,
            "errors": [],
            "warnings": [],
            "file_info": {}
        }
        
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                validation_result["valid"] = False
                validation_result["errors"].append("File does not exist")
                return validation_result
            
            # Get file size
            file_size = os.path.getsize(file_path)
            validation_result["file_info"]["size"] = file_size
            
            # Check file size (10MB limit)
            max_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_size:
                validation_result["valid"] = False
                validation_result["errors"].append(f"File too large: {file_size} bytes (max: {max_size})")
            
            # Validate file type
            allowed_types = ['pdf', 'docx', 'txt', 'png', 'jpg', 'jpeg']
            if file_type.lower() not in allowed_types:
                validation_result["valid"] = False
                validation_result["errors"].append(f"Unsupported file type: {file_type}")
            
            # Additional validations based on file type
            if file_type.lower() == 'pdf':
                try:
                    with open(file_path, 'rb') as file:
                        PyPDF2.PdfReader(file)
                except Exception as e:
                    validation_result["warnings"].append(f"PDF validation warning: {str(e)}")
            
            elif file_type.lower() in ['png', 'jpg', 'jpeg']:
                try:
                    with Image.open(file_path) as image:
                        validation_result["file_info"]["image_dimensions"] = f"{image.width}x{image.height}"
                        validation_result["file_info"]["image_mode"] = image.mode
                except Exception as e:
                    validation_result["warnings"].append(f"Image validation warning: {str(e)}")
            
            return validation_result
            
        except Exception as e:
            validation_result["valid"] = False
            validation_result["errors"].append(f"Validation error: {str(e)}")
            return validation_result
    
    async def preprocess_text(self, text: str) -> str:
        """Preprocess extracted text for better analysis"""
        
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = ' '.join(text.split())
        
        # Remove common OCR artifacts
        text = text.replace('|', 'I')  # Common OCR mistake
        text = text.replace('0', 'O')  # In certain contexts
        
        # Normalize line breaks
        text = text.replace('\n\n', '\n')
        
        return text.strip()
