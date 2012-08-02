from django.contrib.contenttypes.models import ContentType
from django.db.models import Model
from django.utils.translation import ugettext as _

import models

def notify(message, key, target_object=None, url=None):
    """
    Notify subscribing users of a new event. Key can be any kind of string,
    just make sure to reuse it where applicable! Object_id is some identifier
    of an object, for instance if a user subscribes to a specific comment thread,
    you could write:
    
    notify("there was a response to your comment", "comment_response", 
           target_object=PostersObject, 
           url=reverse('comments:view', args=(PostersObject.id,)))
    
    The below example notifies everyone subscribing to the "new_comments" key
    with the message "New comment posted".
    
    notify("New comment posted", "new_comments")
    
    """
    
    if target_object:
        if not isinstance(target_object, Model):
            raise TypeError(_(u"You supplied a target_object that's not an instance of a django Model."))
        object_id = target_object.id
        content_type = ContentType.get_object_for_this_type(target_object)
    else:
        object_id = None
        content_type = None
        
    objects = models.Notification.create_notifications(key, object_id=object_id, 
                                                       content_type=content_type)
    return len(objects)
    