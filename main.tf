provider "aws" {
  region = "us-east-1"
}

# --- 1. DEPOLAMA (S3 BUCKET) ---
resource "aws_s3_bucket" "photo_bucket" {
  # BURAYI KENDİNE GÖRE DEĞİŞTİR (Benzersiz olsun)
  bucket = "oytun-fotograf-portfolyo-2025-v1" 

  tags = {
    Name        = "Oytun Photography"
    Environment = "Portfolio"
  }
}

resource "aws_s3_bucket_ownership_controls" "sahiplik" {
  bucket = aws_s3_bucket.photo_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

# --- 2. GÜVENLİK (CLOUDFRONT OAC) ---
resource "aws_cloudfront_origin_access_control" "photo_oac" {
  name                              = "Foto-Erisim-Karti"
  description                       = "S3 Kova Erisimi"
  origin_access_control_origin_type = "s3"
  signing_behavior                  = "always"
  signing_protocol                  = "sigv4"
}

# --- 3. DAĞITIM (CLOUDFRONT) ---
resource "aws_cloudfront_distribution" "photo_distribution" {
  
  origin {
    domain_name              = aws_s3_bucket.photo_bucket.bucket_regional_domain_name
    origin_id                = "S3-Foto-Galeri"
    origin_access_control_id = aws_cloudfront_origin_access_control.photo_oac.id
  }

  enabled             = true
  default_root_object = "index.html" # Siteye girenler direkt galeriyi görsün

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = "S3-Foto-Galeri"

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

# --- 4. İZİN POLİTİKASI (BUCKET POLICY) ---
resource "aws_s3_bucket_policy" "bucket_policy" {
  bucket = aws_s3_bucket.photo_bucket.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid       = "AllowCloudFront"
        Effect    = "Allow"
        Principal = {
          Service = "cloudfront.amazonaws.com"
        }
        Action    = "s3:GetObject"
        Resource  = "${aws_s3_bucket.photo_bucket.arn}/*"
        Condition = {
          StringEquals = {
            "AWS:SourceArn" = aws_cloudfront_distribution.photo_distribution.arn
          }
        }
      }
    ]
  })
}

# --- 5. ÇIKTI ---
output "site_adresi" {
  value = aws_cloudfront_distribution.photo_distribution.domain_name
}