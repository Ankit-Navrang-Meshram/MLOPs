from fastapi import FastAPI , Path , HTTPException , Query
from app.schemas import PostCreate

app = FastAPI()

text_post = {
    1 : {"title" : "First Post" , "content" : "This is the content of first post"},
    2 : {"title" : "Second Post" , "content" : "This is the content of second post"},
    3 : {"title" : "Third Post" , "content" : "This is the content of third post"} ,
    4 : {"title" : "Fourth Post" , "content" : "This is the content of fourth post"},
    5 : {"title" : "Fifth Post" , "content" : "This is the content of fifth post"},
    6 : {"title" : "Sixth Post" , "content" : "This is the content of sixth post"},
    7 : {"title" : "Seventh Post" , "content" : "This is the content of seventh post"},
    8 : {"title" : "Eighth Post" , "content" : "This is the content of eighth post"},
    9 : {"title" : "Ninth Post" , "content" : "This is the content of ninth post"},
    10 : {"title" : "Tenth Post" , "content" : "This is the content of tenth post"},
}

@app.get("/posts")
def get_all_posts(limit : int = Query(None , description = "Provide the limit up to which you want to see the data")):
    l = list(text_post.values())
    if limit >= len(l):
        return HTTPException(400 , detail = "limit exceed ...")
    if limit : 
        return l[:limit]
    return text_post

@app.get("/posts/{post_id}")
def get_post(post_id: int = Path(..., description="The ID of the post to retrieve" , gt=0)):
    if post_id not in text_post:
        raise HTTPException(status_code=404 , detail="Post not found")
    return text_post[post_id]

@app.post("/posts")
def create_post(post : PostCreate):
    new_post = {"title" : post.title , "content" : post.content}
    text_post[max(text_post.keys())+1] = new_post
    return new_post 
    