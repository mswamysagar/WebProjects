from . import models
from rest_framework import serializers
from authentication import serializers as auth_serializer
from authentication import models as auth_models
from datetime import datetime
import pytz
from django.conf import settings

class StaffSerializer(serializers.ModelSerializer):
    total_assignments = serializers.IntegerField()
    class Meta:
        model = auth_models.CustomUser
        fields=['full_name', 'email','mobile', 'address', 'joining', "raw_pass_code",'id',"logged_device_id", 'image','working_days' ,'designation','age','gender',"total_assignments", 'created_time']

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = request.build_absolute_uri(obj.image.url) if obj.image else ''
        return image_url

class StaffUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.CustomUser
        fields = ['id', 'full_name', 'email', 'mobile', 'salary', 'image', 'total_assignment',"logged_device_id", 'joining']

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = request.build_absolute_uri(obj.image.url) if obj.image else ''
        return image_url

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields= '__all__'

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Patient
        fields = ['id', 'uid', 'created_time', 'last_modified', 'patient_name', 
                  'gender', 'age', 'doctor_name', 'hospital_name', 'mobile', 'email', 'address', 'near_by_landmark', 'patient_status', 'remarks' ]
    
class ExpenseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExpenseType
        fields = ['expense_name', 'uid']

class DropPatientSerializer(serializers.ModelSerializer):
    # patient = serializers.SerializerMethodField()
    class Meta:
        model = models.Patient
        fields = ['patient_name', 'uid']


class AdminIncomeSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.patient_name')
    treatment = serializers.CharField(source='service.treatment_name')
    staff = serializers.CharField(source='staff.full_name')

    class Meta:
        model = models.Payments
        fields = ['patient','treatment','total_amount','staff','payment_method','order_id']

# class PatientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Patient
#         fields = ['uid','patient_name','gender','age','diagnosis','mobile','address']

class StockAssignSerializer(serializers.ModelSerializer):
    products = serializers.CharField(source='products.product_name')
    class Meta:
        model=models.AssignStock
        fields=['uid', 'products', 'quantity']

class AssignmentSerializer(serializers.ModelSerializer):
    treatment = serializers.CharField(source='treatment.treatment_name')
    agent_assigned =serializers.CharField(source='agent_assigned.full_name')
    amount = serializers.CharField(source='treatment.price')
    # product = serializers.CharField(source='product.product_name')
    # scheduled_time = serializers.TimeField(format="%H:%M")
    patient = serializers.CharField(source='patient.patient_name')
    assign_stock = serializers.SerializerMethodField()
    # quantity = serializers.IntegerField(source ='product.quantity')
    # j               = serializers.SerializerMethodField()
    class Meta:
        model = models.Assignments
        fields = ['uid','patient','status','agent_assigned','treatment',"due_date",'amount',"task_id", "arranged_time", 'created_time','assign_stock'] #change name scheduled_time

    def get_assign_stock(self, obj):
        assign_stocks = models.AssignStock.objects.filter(assignment=obj)
        return StockAssignSerializer(assign_stocks, many=True).data
    # def validate_quantity(self, value):
    #     """Custom validation to ensure quantity is valid."""
    #     if value is not None and value < 0:
    #         raise serializers.ValidationError("Quantity cannot be negative.")
    #     return value

    # def get_quantity(self, obj):
    #     if obj.quantity:
    #         return obj.product.quantity
    #     return None
    # def get_patient(self,obj):
    #     return PatientSerializer(obj.patient).data['patient_name']

    # def get_created_at(self,obj):
    #     return obj.created_at.strftime('%Y-%m-%d')
    
    # def get_scheduled_time(self, obj):
    #     return obj.scheduled_time.strftime('%H:%M')

    # def get_arranged_time(self):
    #     india_tz = pytz.timezone(settings.TIME_ZONE)
    #     return self.scheduled_time.astimezone(india_tz)


class TaskAssignmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.patient_name')
    patient_id = serializers.UUIDField(source='patient.uid')
    treatment = serializers.CharField(source='treatment.treatment_name')
    address = serializers.CharField(source='patient.address')
    received_stock = serializers.SerializerMethodField()

    class Meta:
        model = models.Assignments
        fields = ['patient_name', 'treatment', 'address','patient_id','uid', 'status','received_stock']

    def get_received_stock(self, obj):
        assign_stocks = models.AssignStock.objects.filter(assignment=obj)
        return StockAssignSerializer(assign_stocks, many=True).data    
    
class MyAssignmentSerializer(serializers.ModelSerializer):
    patient = serializers.SerializerMethodField()
    class Meta:
        model = models.Assignments
        fields = '__all__'
    def get_patient(self,obj):
        return PatientSerializer(obj.patient).data

class LeaveSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()
    class Meta:
        model = models.Leaves
        fields = ['id', "uid" ,'staff', 'date_from', 'date_to', 'reason','status','name'] # check with __all__
    def get_staff(self,obj):
        return auth_serializer.UserProfileSerializer(obj.staff).data['id']

class TreatmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ['uid','treatment_name']

class LocationTrackingSerializer(serializers.ModelSerializer):
    staff = serializers.CharField(source="staff.full_name")
    image = serializers.SerializerMethodField()

    class Meta:
        model = models.LocationTracking
        fields = ['latitude', "longitude", "location", 'staff', 'image']

    # def get_staff(self,obj):
    #     staff_ser = None
    #     print("self", obj.staff.full_name)
    #     if obj.staff:
    #         staff_ser = auth_serializer.UserProfileSerializer(obj.staff).data['full_name']
    #         print("self", staff_ser)
    #     return staff_ser
    
    def get_image(self, obj):
        request = self.context.get('request')
        image_url = request.build_absolute_uri(obj.staff.image.url) if obj.staff.image else ''
        return image_url

# class AttendanceSerializer(serializers.ModelSerializer):
#     staff = serializers.CharField(source="staff.full_name")
#     punch_in_time=serializers.DateTimeField(format="%H:%M")
#     punch_out_time=serializers.DateTimeField(format="%H:%M")
#     class Meta:
#         model = models.Attendance
#         fields = ['punch_in_time', "punch_in_latitude", "punch_out_longitude", "punch_in_longitude" ,"punch_out_latitude" ,'punch_out_time','work_time','staff','created_time']
#     # def get_staff(self,obj):
#     #     print("self", obj.staff.full_name)
#     #     return auth_serializer.UserProfileSerializer(obj.staff).data['full_name']

class AttendanceSerializer(serializers.ModelSerializer):
    # staff = serializers.SerializerMethodField()
    punch_in_time=serializers.DateTimeField(format="%H:%M")
    punch_out_time=serializers.DateTimeField(format="%H:%M")
    staff = serializers.CharField(source ='staff.full_name')
    class Meta:
        model = models.Attendance
        fields = ['punch_in_time', "punch_in_latitude", "punch_out_longitude", "punch_in_longitude" ,"punch_out_latitude" ,'punch_out_time','work_time','staff']
    # def get_staff(self,obj):
    #     return auth_serializer.UserProfileSerializer(obj.staff).data

class StaffSerializerDetail(serializers.ModelSerializer):
    class Meta:
        model = auth_models.CustomUser
        fields =['full_name', "email", "mobile", "image","dob"]

class ExpenseSerializer(serializers.ModelSerializer):
    staff=serializers.SerializerMethodField()
    class Meta:
        model = models.Expenses
        fields = ['id','staff','created_time','reason','amount', 'status']
    def get_image(self, obj):
        request = self.context.get('request')
        image_url = request.build_absolute_uri(obj.image.url) if obj.image else ''
        return image_url
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = instance.staff.full_name 
        representation['designation']= instance.staff.designation

        del representation['staff']
        print(representation)
        return representation
    
class DateOnlyField(serializers.Field):
    def to_representation(self, value):
        if value:
            if isinstance(value, datetime):
                return value.strftime('%Y-%m-%d')
        return None

class MyExpenseSerializer(serializers.ModelSerializer):
    # created_at = DateOnlyField()  
    reason = serializers.CharField(source='reason.expense_name')
    time = serializers.SerializerMethodField()
    # created_at = serializers.SerializerMethodField()

    class Meta:
        model = models.Expenses
        fields = ['id','staff','created_time','reason','amount', 'time', 'status', "image"]
    
    def get_time(self,obj):
        return obj.time.strftime('%H:%M')
    
    # def get_created_time(self,obj):
    #     return obj.created_at.strftime('%Y-%m-%d')

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['full_name'] = instance.staff.full_name # Display staff's full name instead of just the ID
        representation['designation']= instance.staff.designation
       
        del representation['staff']  # If you don't want to display the 'staff' field directly
        print(representation)
        return representation

class StaffDropSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.CustomUser
        fields = ['id', 'full_name']

class SinglePatientSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()

    class Meta:
        model = models.Patient
        fields = ['patient_name', 'mobile', 'address', 'diagnosis', "price"]

    def get_price(self, obj):
        return ServiceSerializer(obj.diagnosis).data["price"]
    
class PaymentSerializer(serializers.ModelSerializer):
    patient = serializers.CharField(source='patient.patient_name')
    treatment = serializers.CharField(source='service.treatment_name')
    # created_at = serializers.SerializerMethodField()
    # time = serializers.SerializerMethodField()
    # created_at = serializers.SerializerMethodField()
    # time = serializers.SerializerMethodField()

    class Meta:
        model = models.Payments
        fields = ['patient','treatment','total_amount', 'payment_method','created_time','order_id','image']

    # def get_created_at(self, obj):
    #     return obj.created_at.strftime('%Y-%m-%d')

    # def get_time(self, obj):
    #     return self.created_time.strftime('%H:%M')
    
class AdminViewAttendanceSerializer(serializers.ModelSerializer):
    staff = serializers.SerializerMethodField()
    # punch_in_time=serializers.DateTimeField(format="%H:%M")
    # punch_out_time=serializers.DateTimeField(format="%H:%M")
    class Meta:
        model = models.Attendance
        fields = ['punch_in_tm','punch_out_tm','work_tm','staff']
    def get_staff(self,obj):
        return auth_serializer.UserProfileSerializer(obj.staff).data
    def to_representation(self, instance):
        representation=super().to_representation(instance)
        representation['staff']=instance.staff.full_name
        qset = models.Assignments.objects.filter(agent_assigned=instance.staff,status='in_progress',due_date=datetime.now().date()).first()
        representation['working_status'] = bool(qset)
        return representation

class AssignmentSerializerDash(serializers.ModelSerializer): # dashboard
    staff_id = serializers.IntegerField(source='id', read_only=True)  # Get staff ID

    class Meta:
        model = models.Assignments
        fields = ['id', 'status', 'staff_id']  

class StaffAssignmentSerializer(serializers.ModelSerializer):
    amount = serializers.CharField(source='treatment.price')
    treatment = serializers.CharField(source='treatment.treatment_name')
    treatment_id = serializers.CharField(source='treatment.uid')
    patient_id = serializers.CharField(source='patient.uid')
    patient = serializers.CharField(source='patient.patient_name')
    landmark = serializers.CharField(source='patient.near_by_landmark')
    agent_assigned = serializers.CharField(source='agent_assigned.full_name')
    time_taken = serializers.SerializerMethodField()


    # time_taken = serializers.CharField(source='treatment.price')
    class Meta:
        model = models.Assignments
        fields = ['patient','status','agent_assigned','due_date','amount','treatment',"patient_id","treatment_id",'landmark','time_taken']

    # def get_patient(self,obj):
    #     return PatientSerializer(obj.patient).data
    


    def get_time_taken(self, obj):

        # date1 = obj.treatment_started_at
        # date2 = obj.treatment_ended_at
        # time_difference = date2-date1
        # total_seconds = int(time_difference.total_seconds())
        # hours, remainder = divmod(total_seconds, 3600)
        # minutes, seconds = divmod(remainder, 60)
        # formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
        # return formatted_time

        time_format =  "%H:%M:%S"
        time1_obj = datetime.strptime(obj.treatment_started_at.strftime("%H:%M:%S"), time_format)
        time2_obj = datetime.strptime(obj.treatment_ended_at.strftime("%H:%M:%S"), time_format)
        time_difference = time2_obj - time1_obj
        total_seconds = int(time_difference.total_seconds())

        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        # Format the result as hh:mm:ss
        formatted_time_difference = f"{hours:02}:{minutes:02}"

        return formatted_time_difference



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth_models.CustomUser
        fields = ['full_name', 'image']  # Only expose image and basic info
    def update(self, instance, validated_data):
        # Handle image update
        image = validated_data.pop('image', None)
        if image:
            instance.image = image
        instance.save()
        return instance
    
# class DoctorDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Doctor
#         fields = "__all__"

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StockManage
        fields=  ['product_name','quantity','uid','created_time']

# class AttendanceStatusSerializer(serializers.ModelSerializer):
#     status = serializers.SerializerMethodField()
#     class Meta:
#         model = models.Attendance
#         fields = ['status']
    
#     def get_status(self, obj):
#         return obj.get_status_display()

class AttendanceStatusSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()

    class Meta:
        model = models.Attendance
        fields = ['status']
    
    # def get_status(self, obj):
    #     if obj.punch_out_time is None:
    #         return "Punch in"
    #     else:
    #         return "Punch out"
    def get_status(self, obj):
        return obj.get_status_display()
    
class AssignStockSerializer(serializers.ModelSerializer):
    products = serializers.CharField(source='products.product_name')
    class Meta:
        model = models.AssignStock
        fields = ['uid','products','quantity']