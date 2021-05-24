from flask import jsonify, request
from flask.views import MethodView
import app
import errors
from models import User, Post
from schema import POSTS_SCHEMA, USER_CREATE
from validator import validate

class UserView(MethodView):

    def get(self, user_id):
        user = User.by_id(user_id)
        return jsonify(user.to_dict())


    @validate('json', USER_CREATE)
    def post(self):
        user = User(**request.json)
        user.add()
        return jsonify(user.to_dict())


class PostsView(MethodView):

    def get(self, post_id):
        post = Post.by_id(post_id)
        return jsonify(post.to_dict())

    @validate("json", POSTS_SCHEMA)
    def post(self):
        post_positions = [POSTS_SCHEMA["properties"].keys()]
        if request.json.keys() not in post_positions:
            raise errors.BadLuck
        post = Post(**request.json)
        post.add()
        return jsonify(post.to_dict())

    def delete(self, post_id=None):
        get = Post.by_id(post_id)
        if not get:
            raise errors.NotFound
        Post.query.filter_by(id=post_id).delete()
        app.db.session.commit()
        return jsonify({"status": "deleted"})


app.app.add_url_rule('/users/<int:user_id>', view_func=UserView.as_view('users_get'), methods=['GET', ])
app.app.add_url_rule('/users/', view_func=UserView.as_view('users_create'), methods=['POST', ])
app.app.add_url_rule('/posts/<int:post_id>', view_func=PostsView.as_view('posts_get'), methods=['GET', ])
app.app.add_url_rule('/posts/', view_func=PostsView.as_view('posts_post'), methods=['POST', ])
app.app.add_url_rule('/posts/<int:post_id>', view_func=PostsView.as_view('posts_delete'), methods=['DELETE', ])