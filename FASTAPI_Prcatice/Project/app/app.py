from fastapi import FastAPI , Path , HTTPException , Query , File , UploadFile , Form , Depends
from app.schemas import PostCreate , PostResponse
from app.db import Post, create_db_and_tables , get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import shutil
import os
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app : FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan = lifespan)




@app.post("/upload")
async def upload_file(
    file : UploadFile = File(...),
    caption : str = Form(""),
    session : AsyncSession = Depends(get_async_session)
):
    temp_file_path = None
    try:
        with tempfile.NamedTemporaryFile(delete = False , suffix = os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path = temp_file.name
            shutil.copyfileobj(file.file , temp_file)

        upload_result = imagekit.upload_file(
            file = open(temp_file_path , 'rb'),
            file_name = file.filename,
            options = UploadFileRequestOptions(
                use_unique_file_name = True,
                tags = ["backend-upload"]
            )
        )

        if upload_result.response_metadata.http_status_code == 200 :
            post = Post(
                caption = caption,
                url = upload_result.url,
                file_type = "video" if file.content_type.startswith("video/") else "image",
                file_name = upload_result.name
            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
    except Exception as e:
        raise HTTPException(status_code = 500 , detail = str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()

@app.get("/feed")
async def get_feed(
    session : AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    post_data = []

    for post in posts:
        post_data.append(
            {
                "id" : str(post.id),
                "caption" : post.caption , 
                "url" : post.url,
                "file_type" : post.file_type,
                "file_name" : post.file_name,
                "created_at" : post.created_at.isoformat()
            }
        )
    return {"posts" : post_data}




# stage 2 : with database usage example 

# @app.post("/upload")
# async def upload_file(
#     file : UploadFile = File(...),
#     caption : str = Form(""),
#     session: AsyncSession = Depends(get_async_session)
# ):
#     post = Post(
#         caption = caption,
#         url = "dummy url",
#         file_type = "photo",
#         file_name = "dummy name"
#     )

#     session.add(post)
#     await session.commit()
#     await session.refresh(post)
#     return post


# @app.get("/feed")
# async def get_feed(
#     session : AsyncSession = Depends(get_async_session)
# ):
#     result = await session.execute(select(Post).order_by(Post.created_at.desc()))
#     posts = [row[0] for row in result.all()]

#     post_data = []

#     for post in posts:
#         post_data.append(
#             {
#                 "id" : str(post.id),
#                 "caption" : post.caption , 
#                 "url" : post.url,
#                 "file_type" : post.file_type,
#                 "file_name" : post.file_name,
#                 "created_at" : post.created_at.isoformat()
#             }
#         )
#     return {"posts" : post_data}










# stage 1 : without  database

# text_post = {
#     1 : {"title" : "First Post" , "content" : "This is the content of first post"},
#     2 : {"title" : "Second Post" , "content" : "This is the content of second post"},
#     3 : {"title" : "Third Post" , "content" : "This is the content of third post"} ,
#     4 : {"title" : "Fourth Post" , "content" : "This is the content of fourth post"},
#     5 : {"title" : "Fifth Post" , "content" : "This is the content of fifth post"},
#     6 : {"title" : "Sixth Post" , "content" : "This is the content of sixth post"},
#     7 : {"title" : "Seventh Post" , "content" : "This is the content of seventh post"},
#     8 : {"title" : "Eighth Post" , "content" : "This is the content of eighth post"},
#     9 : {"title" : "Ninth Post" , "content" : "This is the content of ninth post"},
#     10 : {"title" : "Tenth Post" , "content" : "This is the content of tenth post"},
# }

# @app.get("/posts")
# def get_all_posts(limit : int = Query(... , description = "Provide the limit up to which you want to see the data")) -> list[PostResponse]:
#     l = text_post.values()
#     if limit > len(l):
#         return HTTPException(status_code = 404 , detail="Limit Exceed ...") 
#     l = [PostResponse(**k) for k in l]
#     return l[:limit]
    

# @app.get("/posts/{post_id}")
# def get_post(post_id: int = Path(..., description="The ID of the post to retrieve" , gt=0)) -> PostResponse:
#     if post_id not in text_post:
#         raise HTTPException(status_code=404 , detail="Post not found")
#     return PostResponse(**text_post[post_id])

# @app.post("/posts")
# def create_post(post : PostCreate) -> PostResponse:
#     new_post = {"title" : post.title , "content" : post.content}
#     text_post[max(text_post.keys())+1] = new_post
#     return PostResponse(**new_post)



