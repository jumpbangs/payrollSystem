from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from backend.networkHelpers import (
    get_error_response_400,
    get_server_response_500,
    get_success_response_200,
    get_success_response_201,
)
from backend.utils.helpers import is_none_or_empty, is_upper_management
from employee.models import Employee, Teams
from employee.serializers import TeamDetailSerializer, TeamsListSerializer


class TeamsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    """
    GET: Fetches all teams/team members for the given team id
    """

    def get(self, request):
        if not is_upper_management(request.user.user_role):
            return get_error_response_400("Only upper management are allow to fetch teams")

        team_id = request.query_params.get("team_id") or None

        if team_id is not None:
            try:
                team_detail = Teams.objects.filter(team_id=team_id).first()
                if not team_detail:
                    return get_error_response_400("Following team does not exist")

                serialized_team_detail = TeamDetailSerializer(team_detail)
                return get_success_response_200(serialized_team_detail.data)
            except Exception as exception:
                return get_server_response_500(f"Exception when fetching team detail: {str(exception)}")

        else:
            try:
                team_list = Teams.objects.all()
                serialized_team_list = TeamsListSerializer(team_list, many=True)

                return get_success_response_200(serialized_team_list.data)

            except Exception as exception:
                return get_server_response_500(f"Exception when fetching team : {str(exception)}")

    """
    POST: Create a new team
    """

    def post(self, request):
        if not is_upper_management(request.user.user_role):
            return get_error_response_400("Only upper management are allow to create teams")

        team_data = request.data
        required_fields = ["team_name", "description"]

        missing_fields = [field for field in required_fields if field not in team_data]
        if missing_fields:
            return get_error_response_400(f"Missing fields: {', '.join(missing_fields)}")

        if Teams.objects.filter(team_name=team_data.get("team_name")).exists():
            return get_error_response_400("Team with the same name already exists")

        try:
            serialized_team_data = TeamDetailSerializer(data=team_data)
            if serialized_team_data.is_valid():
                serialized_team_data.save()
                return get_success_response_201(serialized_team_data.data)
            else:
                return get_error_response_400("Failed to create team")

        except Exception as exception:
            return get_server_response_500(f"Exception when creating team: {str(exception)}")

    """
    PATCH: Update team details
    """

    def patch(self, request):
        if not is_upper_management(request.user.user_role):
            return get_error_response_400("Only upper management are allow to update teams")

        team_data = request.data
        team_id = team_data.get("team_id")

        if is_none_or_empty(team_id):
            return get_error_response_400("Team id cannot be empty")

        try:
            team_to_update = Teams.objects.get(team_id=team_id)
            new_member_ids = team_data.get("members", [])

            if new_member_ids:
                employees = Employee.objects.filter(user_id__in=new_member_ids)
                team_to_update.members.add(*employees)

            serialized_team_data = TeamDetailSerializer(team_to_update, data=team_data, partial=True)

            if serialized_team_data.is_valid():
                serialized_team_data.save()
                return get_success_response_200(serialized_team_data.data)
            else:
                return get_error_response_400("Failed to update team")

        except Teams.DoesNotExist:
            return get_error_response_400("Following team does not exist")

        except Exception as exception:
            return get_server_response_500(f"Exception when updating team: {str(exception)}")

    """
    DELETE: Delete a team
    """

    def delete(self, request):
        if not is_upper_management(request.user.user_role):
            return get_error_response_400("Only upper management are allow to delete teams")

        team_id = request.query_params.get("team_id")

        if is_none_or_empty(team_id):
            return get_error_response_400("Team id cannot be empty")

        try:
            team_to_delete = Teams.objects.get(team_id=team_id)
            team_to_delete.delete()
            return get_success_response_200("Team has been deleted")
        except Teams.DoesNotExist:
            return get_error_response_400("Following team does not exist")
        except Exception as exception:
            return get_server_response_500(f"Exception when deleting team: {str(exception)}")
