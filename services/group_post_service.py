from typing import List, Optional, Dict, Any
from repositories.group_post_repository import GroupPostRepository
from repositories.group_repository import GroupRepository
from schemas.group_post_schemas import GroupPostCreate, GroupPostUpdate
from utils.exceptions import PermissionDeniedError, NotFoundError, ValidationError
import logging

logger = logging.getLogger(__name__)

class GroupPostService:
    def __init__(self, post_repo: GroupPostRepository, group_repo: GroupRepository):
        self.post_repo = post_repo
        self.group_repo = group_repo
    
    def create_post(self, post_data: GroupPostCreate, author_id: int) -> Dict[str, Any]:
        """Create a new post in a group"""
        # Verify group exists and user is a teacher member
        group = self.group_repo.get_group_by_id(post_data.group_id)
        if not group:
            raise NotFoundError(f"Group {post_data.group_id} not found")
        
        # Check if user is a teacher in the group
        user_role = self.group_repo.get_member_role(post_data.group_id, author_id)
        if user_role != "teacher":
            raise PermissionDeniedError("Only teachers can create posts")
        
        # Validate link posts
        if post_data.post_type == "link" and not post_data.link_url:
            raise ValidationError("Link posts must include a URL")
        
        # Create post
        post_dict = post_data.dict()
        post_dict.update({"author_id": author_id})
        
        post = self.post_repo.create_post(post_dict)
        
        return {
            "id": post.id,
            "title": post.title,
            "post_type": post.post_type,
            "created_at": post.created_at,
            "group_name": group.name
        }
    
    def get_group_posts(
        self, 
        group_id: int, 
        user_id: int,
        post_type: str = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """Get all posts in a group that a user can access"""
        # Verify group exists and user is a member
        group = self.group_repo.get_group_by_id(group_id)
        if not group:
            raise NotFoundError(f"Group {group_id} not found")
        
        is_member = self.group_repo.is_group_member(group_id, user_id)
        if not is_member:
            raise PermissionDeniedError("You are not a member of this group")
        
        # Get posts
        posts = self.post_repo.get_group_posts(group_id, post_type, limit, offset)
        total_posts = self.post_repo.count_group_posts(group_id)
        
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                "id": post.id,
                "title": post.title,
                "content": post.content,
                "post_type": post.post_type,
                "link_url": post.link_url,
                "link_description": post.link_description,
                "author_name": post.author.full_name,
                "author_email": post.author.email,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            })
        
        return {
            "group_id": group_id,
            "group_name": group.name,
            "posts": formatted_posts,
            "total_posts": total_posts,
            "has_more": (offset + len(posts)) < total_posts
        }
    
    def update_post(
        self, 
        post_id: int, 
        update_data: GroupPostUpdate, 
        user_id: int
    ) -> Dict[str, Any]:
        """Update a post (only by author)"""
        post = self.post_repo.get_post_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")
        
        # Verify user is the author
        if post.author_id != user_id:
            raise PermissionDeniedError("You can only edit your own posts")
        
        # Update post
        updated = self.post_repo.update_post(post_id, update_data.dict(exclude_unset=True))
        
        return {
            "id": updated.id,
            "title": updated.title,
            "updated_at": updated.updated_at
        }
    
    def delete_post(self, post_id: int, user_id: int) -> bool:
        """Delete a post (only by author or group teacher)"""
        post = self.post_repo.get_post_by_id(post_id)
        if not post:
            raise NotFoundError(f"Post {post_id} not found")
        
        # Check if user is the author
        if post.author_id == user_id:
            return self.post_repo.delete_post(post_id)
        
        # Check if user is a teacher in the group
        user_role = self.group_repo.get_member_role(post.group_id, user_id)
        if user_role == "teacher":
            return self.post_repo.delete_post(post_id)
        
        raise PermissionDeniedError("You don't have permission to delete this post")
    
    def get_teacher_posts(self, teacher_id: int, group_id: int = None) -> List[Dict[str, Any]]:
        """Get all posts by a teacher"""
        posts = self.post_repo.get_teacher_posts(teacher_id, group_id)
        
        formatted_posts = []
        for post in posts:
            formatted_posts.append({
                "id": post.id,
                "title": post.title,
                "post_type": post.post_type,
                "group_name": post.group.name,
                "created_at": post.created_at,
                "updated_at": post.updated_at
            })
        
        return formatted_posts