"""AWS S3 service integration."""
from app.core.config import settings
from app.core.logging import get_logger
from typing import Optional

logger = get_logger(__name__)


class S3Service:
    """Service for AWS S3 file storage integration."""
    
    def __init__(self):
        """Initialize S3 service."""
        self.enabled = settings.USE_S3
        if self.enabled:
            try:
                import boto3
                from botocore.exceptions import ClientError
                import uuid
                
                self.s3_client = boto3.client(
                    's3',
                    region_name=settings.AWS_REGION,
                    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
                )
                self.bucket_name = settings.S3_BUCKET_NAME
                self.uuid = uuid
                self.ClientError = ClientError
                logger.info("S3 service initialized")
            except ImportError:
                self.enabled = False
                logger.warning("boto3 not installed, S3 service disabled")
            except Exception as e:
                self.enabled = False
                logger.error(f"Failed to initialize S3 service: {str(e)}")

    async def upload_file(self, file_content: bytes, filename: str) -> Optional[str]:
        """
        Upload file to S3 in production, return local path in development.
        
        Args:
            file_content: File content as bytes
            filename: Original filename
            
        Returns:
            S3 key or local filename
        """
        if not self.enabled:
            # Local development - just return filename
            return filename
        
        try:
            # Production - upload to S3
            file_extension = filename.split('.')[-1] if '.' in filename else ''
            s3_key = (
                f"documents/{self.uuid.uuid4()}.{file_extension}"
                if file_extension
                else f"documents/{self.uuid.uuid4()}"
            )
            
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=s3_key,
                Body=file_content,
                ContentType=self._get_content_type(filename)
            )
            
            logger.info(f"File uploaded to S3: {s3_key}")
            return s3_key
        except Exception as e:
            logger.error(f"Error uploading to S3: {str(e)}")
            return None

    def _get_content_type(self, filename: str) -> str:
        """
        Get content type based on file extension.
        
        Args:
            filename: File filename
            
        Returns:
            MIME content type
        """
        extension = filename.split('.')[-1].lower() if '.' in filename else ''
        content_types = {
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'doc': 'application/msword',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png'
        }
        return content_types.get(extension, 'application/octet-stream')

    def get_file_url(self, s3_key: str) -> str:
        """
        Generate presigned URL for production, return filename for development.
        
        Args:
            s3_key: S3 object key
            
        Returns:
            Presigned URL or local file path
        """
        if not self.enabled:
            return f"/local/files/{s3_key}"
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': s3_key},
                ExpiresIn=3600
            )
            return url
        except Exception as e:
            logger.error(f"Error generating S3 presigned URL: {str(e)}")
            return ""


# Global instance
s3_service = S3Service()

