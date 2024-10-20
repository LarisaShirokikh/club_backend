from celery import Celery
import celery
from flask import current_app
import vk_api
from datetime import datetime

def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    return celery

def fetch_posts():
    @celery.task
    def fetch_favorites_task():
        vk_session = vk_api.VkApi(token=current_app.config['VK_API_TOKEN'])
        vk = vk_session.get_api()

        try:
            response = vk.fave.getPosts()
            posts = response['items']
            
            formatted_posts = [
                {
                    "post_id": post['id'],
                    "owner_id": post['owner_id'],
                    "text": post.get('text', 'No text'),
                    "date": datetime.fromtimestamp(post['date']).isoformat()
                }
                for post in posts
            ]
            return {"posts": formatted_posts, "posts_count": len(formatted_posts)}
        
        except vk_api.exceptions.ApiError as e:
            return {"status": "failed", "error": str(e)}
    return fetch_favorites_task