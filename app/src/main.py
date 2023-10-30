from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from app.src import database
from app.src import constants

from app.src.auth import AuthRouter
from app.src.users import UsersRouter
from app.src.recipes import RecipesRouter
from app.src.reviews import ReviewsRouter
from app.src.favorites import FavoritesRouter
from app.src.follows import FollowsRouter

database.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title=constants.APP_TITLE, 
              summary=constants.APP_SUMMARY,
              description=constants.APP_DESCRIPTION,
              swagger_ui_parameters={"syntaxHighlight.theme":"obsidian"})


# enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["*"]
)

@app.get("/", include_in_schema=False)
def home_page():
    response = RedirectResponse(url="/docs", status_code=status.HTTP_302_FOUND)
    return response

# Application routers
app.include_router(AuthRouter.router)
app.include_router(UsersRouter.router)
app.include_router(RecipesRouter.router)
app.include_router(ReviewsRouter.router)
app.include_router(FavoritesRouter.router)
app.include_router(FollowsRouter.router)

