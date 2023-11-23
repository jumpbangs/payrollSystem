from rest_framework import status
from rest_framework.response import Response


def get_success_response_200(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_200_OK)


def get_success_response_201(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_201_CREATED)


def get_error_response_400(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_400_BAD_REQUEST)


def get_error_response_403(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_403_FORBIDDEN)


def get_error_response_404(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_404_NOT_FOUND)


def get_server_response_500(data):
    return Response(data={"success": True, "data": data}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
