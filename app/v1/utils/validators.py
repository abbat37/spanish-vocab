"""
Request Validation Schemas
"""
from marshmallow import Schema, fields, validate


class MarkLearnedSchema(Schema):
    """Schema for validating mark-learned API requests"""
    word_id = fields.Integer(required=True, validate=validate.Range(min=1))
