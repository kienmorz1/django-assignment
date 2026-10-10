from django.shortcuts import render
from .models import Reporter, Issue, CriticalIssue, LowPriorityIssue
from .utils import JSONFileHandler
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as stat
from typing import override
import json
# Create your views here.

REPORTER_FILE_NAME="issues/files/reporter.json"


_reporter_file = JSONFileHandler(REPORTER_FILE_NAME)
_issue_file = JSONFileHandler("issues/files/issues.json")



def __get_all_reporters():
    return _reporter_file.read()

def __add_reporter(updated_reporters):
    return _reporter_file.write(updated_reporters)
        

@api_view(['GET','POST'])   
def reporters_mgmt(request):
    if request.method == "GET":
        reporters = __get_all_reporters()
        reporter_id = request.GET.get('id')
        if not reporter_id:
            return JsonResponse(reporters,status=200,safe=False)
        else:
            for reporter in reporters:
                if reporter['id'] == int(reporter_id):
                    return JsonResponse(reporter,safe=False)
            return JsonResponse({"error": f"Reporter ID: {reporter_id} Not Found"},status=stat.HTTP_404_NOT_FOUND)
    elif request.method == "POST":
        current_reporters = __get_all_reporters()
        id = len(current_reporters) + 1
        name = request.data.get('name')
        email = request.data.get('email')
        team = request.data.get('team')
        new_reporter = Reporter(id, name, email, team)
        try:
            new_reporter.validate()
            current_reporters.append(new_reporter.to_dict())
            __add_reporter(current_reporters)
            return Response({"message": f"Reporter {name} added!!"},status=stat.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error":f"{e}"},status=stat.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error":"Invalid Request Method"},status=stat.HTTP_405_METHOD_NOT_ALLOWED)
        


class IssueView(APIView):

    def _get_all_issues(self):
        return _issue_file.read()

    def _add_issues(self,updated_issues):
        return _issue_file.write(updated_issues)

    def _get_issue_by_id(self,id):
        current_issues = self._get_all_issues()
        for issue in current_issues:
            if issue['id'] == id:
                return Response(issue,status=stat.HTTP_200_OK)
        return Response({"Error":f"Issue ID {id} is not found"},status=stat.HTTP_404_NOT_FOUND)
                
    
    def _get_issue_by_status(self,status):
        current_issues = self._get_all_issues()
        filtered_issues = list(filter(lambda x: x['status'] == status, current_issues))
        if not filtered_issues:
            return Response({"Error":f"No Issues are in {status} state"},status=stat.HTTP_404_NOT_FOUND)
        return Response(filtered_issues,status=stat.HTTP_200_OK)

    def get(self,request):
        params = list(request.query_params)
        if len(params) > 1:
            return Response({"error":"Found Multiple Paramaters, Only id or status is supported"},status=stat.HTTP_400_BAD_REQUEST)
        issue_id = request.query_params.get('id')
        status = request.query_params.get('status')
        if not (issue_id or status):
            current_issues = self._get_all_issues()
            return Response(current_issues, status = stat.HTTP_200_OK)
        elif issue_id:
            return self._get_issue_by_id(int(issue_id))
        elif status:
            return self._get_issue_by_status(status)
        else:
            return Response({'Error':'Invalid Request'},status=stat.HTTP_400_BAD_REQUEST)
    
    def post(self,request):
        current_issues = self._get_all_issues()
        id = len(current_issues) + 1
        title = request.data.get('title')
        description = request.data.get('description')
        priority = request.data.get('priority')
        reporter_id = request.data.get('reporter_id')
        if priority.lower() == "critical":
            new_issue = CriticalIssue(id, title, description, priority, reporter_id)
        elif priority.lower() == 'low':
            new_issue = LowPriorityIssue(id, title, description, priority, reporter_id)
        else:
            new_issue = Issue(id, title, description, priority, reporter_id)
        try:
            new_issue.validate()
            response_issue = new_issue.to_dict()
            current_issues.append(response_issue)
            self._add_issues(current_issues)
            response_issue['message'] = new_issue.describe()
            return Response(response_issue,status=stat.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error":f"{e}"},status=stat.HTTP_400_BAD_REQUEST)