# from rest_framework import serializers
# from .models import Student, STAGE_CHOICES
# from .validators import validate_egypt_phone
# from datetime import date

# class StudentSerializer(serializers.ModelSerializer):
#     age = serializers.IntegerField(read_only=True)

#     class Meta:
#         model = Student
#         fields = [
#             "id", "full_name", "email", "phone",
#             "birth_date", "stage", "notes",
#             "age", "created_at", "updated_at",
#         ]
#         read_only_fields = ["created_at", "updated_at", "age"]

#     def validate_email(self, value):
#         value = value.lower().strip()
#         # فريد كيس-إنسنسِتف
#         qs = Student.objects.filter(email__iexact=value)
#         if self.instance:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise serializers.ValidationError("هذا البريد مستخدم من قبل.")
#         return value

#     def validate_phone(self, value):
#         v = validate_egypt_phone(value)
#         qs = Student.objects.filter(phone=v)
#         if self.instance:
#             qs = qs.exclude(pk=self.instance.pk)
#         if qs.exists():
#             raise serializers.ValidationError("هذا الرقم مستخدم من قبل.")
#         return v

#     def validate_stage(self, value):
#         valid = [c[0] for c in STAGE_CHOICES]
#         if value not in valid:
#             raise serializers.ValidationError("قيمة المرحلة غير صحيحة.")
#         return value

#     def validate_birth_date(self, value):
#         if value and value >= date.today():
#             raise serializers.ValidationError("تاريخ الميلاد يجب أن يكون في الماضي.")
#         return value


from rest_framework import serializers
from .models import Student, STAGE_CHOICES
from datetime import date
import re

EG_PHONE_REGEX = re.compile(r"^01[0-2,5][0-9]{8}$")

def validate_egypt_phone(value: str) -> str:
    v = value.strip().replace(" ", "")
    if v.startswith("+2"):
        v = v[2:]
    if not EG_PHONE_REGEX.match(v):
        raise serializers.ValidationError("رقم الهاتف المصري غير صالح. مثال: 01012345678")
    return v

class StudentSerializer(serializers.ModelSerializer):
    age = serializers.IntegerField(read_only=True)

    class Meta:
        model = Student
        fields = ["id","full_name","email","phone","birth_date","stage","notes","age","created_at","updated_at"]
        read_only_fields = ["created_at", "updated_at", "age"]

    def validate_email(self, value):
        value = value.lower().strip()
        qs = Student.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("هذا البريد مستخدم من قبل.")
        return value

    def validate_phone(self, value):
        v = validate_egypt_phone(value)
        qs = Student.objects.filter(phone=v)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("هذا الرقم مستخدم من قبل.")
        return v

    def validate_stage(self, value):
        valid = [c[0] for c in STAGE_CHOICES]
        if value not in valid:
            raise serializers.ValidationError("قيمة المرحلة غير صحيحة.")
        return value

    def validate_birth_date(self, value):
        if value and value >= date.today():
            raise serializers.ValidationError("تاريخ الميلاد يجب أن يكون في الماضي.")
        return value
