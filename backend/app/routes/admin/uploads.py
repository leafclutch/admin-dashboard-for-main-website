# import time
# import hashlib # hashlib is a built-in Python library for generating secure signatures

# from fastapi import APIRouter, Depends
# from app.auth.deps import get_current_user
# from app.config import settings # settings is a module that contains all the configuration variables for the application

# router = APIRouter(
#     prefix="/admin/uploads",
#     tags=["Uploads"],
# )

# # generate signature for cloudinary upload 
# def generate_cloudinary_signature(
#     timestamp: int,
#     folder: str | None = None,
# ) -> str:
#     """
#     Generates a Cloudinary upload signature.

#     Cloudinary requires parameters to be:
#     - alphabetically sorted
#     - concatenated as key=value pairs
#     - signed with API_SECRET
#     """

#     # Step 1: Put the timestamp into a list of data to be signed
#     params = {"timestamp": timestamp}

#     # Step 2: If a folder is provided, add it to the list
#     if folder:
#         params["folder"] = folder

#     # Step 3: Sort the data alphabetically and join them with "&"
#     param_string = "&".join(
#         f"{key}={value}" for key, value in sorted(params.items())
#     )

#     # Step 4: Check if the Cloudinary Secret is set in the .env file
#     if not settings.cloudinary_api_secret:
#         from fastapi import HTTPException
#         raise HTTPException(
#             status_code=500,
#             detail="Cloudinary API Secret is not configured. Please check your .env file."
#         )

#     # Step 5: Combine the sorted data with the Secret Key and create a secure hash (Signature)
#     to_sign = f"{param_string}{settings.cloudinary_api_secret}"
#     signature = hashlib.sha1(to_sign.encode()).hexdigest() 

#     return signature

# # GET /admin/uploads/signature
# @router.post("/signature")
# def get_upload_signature(
#     admin = Depends(get_current_user)
# ):
#     """
#     Returns a Cloudinary signed upload payload.
#     Frontend uses this to upload images directly to Cloudinary.
#     """

#     # Step 1: Get the current time (Cloudinary needs this to prevent old signatures from being reused)
#     timestamp = int(time.time())

#     # Step 2: Set the folder name where the image will be saved
#     folder = "uploads"

#     # Step 3: Generate the secure signature using our helper function above
#     signature = generate_cloudinary_signature(
#         timestamp=timestamp,
#         folder=folder,
#     )

#     # Step 4: Send all the details back to the frontend so it can upload the image
#     return {
#         "cloud_name": settings.cloudinary_cloud_name,
#         "api_key": settings.cloudinary_api_key,
#         "timestamp": timestamp,
#         "signature": signature,
#         "folder": folder,
#     }
