from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_error_response_401,
    get_error_response_403,
    get_error_response_404,
    get_server_response_500,
    get_success_response_200,
    get_success_response_201,
)
from backend.utils.helpers import (
    is_none_or_empty,
    is_user_admin,
    is_user_manager_or_admin,
)
from employee.docs.employee_schema import (
    delete_employee_schema,
    get_employee_schema,
    patch_employee_schema,
    post_employee_schema,
)
from employee.docs.payment_schema import (
    delete_payment_schema,
    get_payment_schema,
    patch_payment_schema,
    post_payment_schema,
)
from employee.docs.term_schema import (
    get_employee_term_schema,
    patch_employee_term_schema,
)
from employee.models import Employee, EmploymentTerms, Payments
from employee.serializers import (
    EmployeeSerializer,
    EmploymentTermsSerializer,
    PaymentsSerializer,
)


# Create your views here.
class EmployeeModelView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetch Employee data by id else fetch all
    """

    @get_employee_schema
    def get(self, request):
        employee_id = request.query_params.get("user_id")
        if is_none_or_empty(employee_id):
            if not is_user_manager_or_admin(request.user.user_role):
                return get_error_response_403("Only admin and manager can fetch all employees")

            try:
                employee_data = Employee.objects.all().exclude(user_id=request.user.user_id)
                serialized_data = EmployeeSerializer(employee_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                employee_data = Employee.objects.filter(user_id=employee_id)
                serialized_data = EmployeeSerializer(employee_data, many=True)
                return get_success_response_200(serialized_data.data)

            except Employee.DoesNotExist:
                return get_error_response_404("Employee not found")
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    POST: Add new Employee
    """

    @post_employee_schema
    def post(self, request):
        employee_data = request.data

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_403("Only admin and manager can add new employees")

        if is_none_or_empty(employee_data):
            return get_error_response_400("Employee data cannot be empty")

        if is_none_or_empty(employee_data.get("email")):
            return get_error_response_400("Employee email cannot be empty")
        else:
            if Employee.objects.filter(email=employee_data.get("email")).exists():
                return get_error_response_400("Employee with this email already exists")

        with transaction.atomic():
            try:
                new_employee = Employee.objects.create(**employee_data)
                new_employee.save()
                new_employee_data = EmployeeSerializer(new_employee)
                return get_success_response_201(new_employee_data.data)

            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    PATCH: Update Employee
    """

    @patch_employee_schema
    def patch(self, request):
        employee_data = request.data
        user_id = employee_data.get("user_id")
        is_allowed_to_update = False

        if is_none_or_empty(employee_data):
            return get_error_response_400("Employee data cannot be empty")

        if is_none_or_empty(user_id):
            return get_error_response_400("Employee id cannot be empty")

        if is_user_manager_or_admin(request.user.user_role):
            is_allowed_to_update = True

        if not is_user_admin(request.user.user_role) and employee_data.get("user_role") is not None:
            return get_error_response_401("Only admin can update employee role")

        try:
            employee_data_to_update: Employee = Employee.objects.get(pk=user_id)
            if employee_data_to_update.user_id != request.user.user_id and not is_allowed_to_update:
                return get_error_response_401("You are can only update your own profile")

            serialized_data = EmployeeSerializer(employee_data_to_update, data=employee_data, partial=True)
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Employee data is invalid")

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE: Delete Employee
    """

    @delete_employee_schema
    def delete(self, request):
        user_id = request.query_params.get("user_id")

        if not is_user_admin(request.user.user_role):
            return get_error_response_401("Only admin can delete employees")

        if is_none_or_empty(user_id):
            return get_error_response_400("Employee id cannot be empty")

        try:
            employee_data_to_delete: Employee = Employee.objects.get(pk=user_id)
            employee_data_to_delete.delete()
            return get_success_response_200("Employee deleted successfully")
        except Employee.DoesNotExist:
            return get_error_response_404("Employee not found")
        except Exception as exception:
            return get_server_response_500(str(exception))


class EmploymentTermsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetch all employment terms
    """

    @get_employee_term_schema
    def get(self, request):
        employee_id = request.query_params.get("employee_id")
        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can fetch all employment terms")

        if is_none_or_empty(employee_id):
            try:
                employment_terms_data = EmploymentTerms.objects.all()
                serialized_data = EmploymentTermsSerializer(employment_terms_data, many=True)
                return get_success_response_200(serialized_data.data)
            except Exception as exception:
                return get_server_response_500(str(exception))
        else:
            try:
                employee_term_data = EmploymentTerms.objects.filter(employee_id=employee_id)
                serialized_data = EmploymentTermsSerializer(employee_term_data, many=False)
                return get_success_response_200(serialized_data.data)
            except Exception as exception:
                return get_server_response_500(str(exception))

    """
    PATCH: Update employment term
    """

    @patch_employee_term_schema
    def patch(self, request):
        employment_term_data = request.data
        employee_id = employment_term_data.get("employee_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and manager can update employment terms")

        if is_none_or_empty(employment_term_data):
            return get_error_response_400("Employment term data cannot be empty")

        if is_none_or_empty(employee_id):
            return get_error_response_400("Employee id cannot be empty")

        try:
            employment_term_data_to_update = EmploymentTerms.objects.get(employee_id=employee_id)
            serialized_data = EmploymentTermsSerializer(
                employment_term_data_to_update, data=employment_term_data, partial=True
            )
            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)
            else:
                return get_error_response_400("Employment term data is invalid")

        except Exception as exception:
            return get_server_response_500(str(exception))


class PaymentView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetch payment view for employee/employees
    """

    @get_payment_schema
    def get(self, request):
        req_employee_id = request.query_params.get("employee_id")

        def get_employee_payment(given_employee_id):
            try:
                employee_payment = Payments.objects.filter(employee_id_id=given_employee_id)
                if not employee_payment.exists():
                    return get_error_response_400("Payment details doesn't exist for the given employee")
                else:
                    serialized_payment = PaymentsSerializer(employee_payment, many=True)
                    return get_success_response_200(serialized_payment.data)

            except Exception as exception:
                return get_server_response_500(str(exception))

        if is_user_admin(request.user.user_role):
            if is_none_or_empty(req_employee_id):
                return get_error_response_400("Employee id is empty.")
            return get_employee_payment(req_employee_id)
        else:
            return get_employee_payment(request.user.user_id) or get_error_response_400(
                "Only admins and users can fetch other/their user payment details"
            )

    """
    POST: Add payment to user detail
    """

    @post_payment_schema
    def post(self, request):
        payment_detail = request.data
        required_fields = ["employee_id", "gross_salary", "net_salary", "tax"]

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and managers can add user payment detail")

        # Check for required fields
        missing_fields = [field for field in required_fields if field not in payment_detail]
        if missing_fields:
            return get_error_response_400(f"Missing fields: {', '.join(missing_fields)}")

        employee_id = payment_detail.get("employee_id")
        try:
            check_employee_data = Payments.objects.filter(employee_id=employee_id)
            if check_employee_data:
                return get_error_response_400("Employee payment details exists")

            serialized_payment = PaymentsSerializer(data=payment_detail)
            if serialized_payment.is_valid():
                serialized_payment.save()
                return get_success_response_201(serialized_payment.data)
            else:
                return get_error_response_400(serialized_payment.errors)
        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    PATCH: Update the user payment detail by the employee_id
    """

    @patch_payment_schema
    def patch(self, request):
        update_details = request.data

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and managers can add user payment detail")

        if "employee_id" not in update_details:
            return get_error_response_400("Employee id is required")

        try:
            req_employee_id = update_details.get("employee_id")
            employee_to_be_updated = Payments.objects.get(employee_id=req_employee_id)
            serialized_data = PaymentsSerializer(employee_to_be_updated, data=update_details, partial=True)

            if serialized_data.is_valid():
                serialized_data.save()
                return get_success_response_200(serialized_data.data)

        except Exception as exception:
            return get_server_response_500(str(exception))

    """
    DELETE : Delete the user payment detail by employee_id
    """

    @delete_payment_schema
    def delete(self, request):
        req_employee_id = request.query_params.get("employee_id")

        if not is_user_manager_or_admin(request.user.user_role):
            return get_error_response_401("Only admin and managers can delete user payment details")

        if req_employee_id is None:
            return get_error_response_400("employee_id is required")

        try:
            employee_payment_detail = Payments.objects.get(employee_id=req_employee_id)
            employee_payment_detail.delete()
            return get_success_response_200("Employee's payment detail has been deleted")

        except Payments.DoesNotExist:
            return get_error_response_404("Given employee's payment detail does not exist")
        except Exception as exception:
            return get_server_response_500(str(exception))
