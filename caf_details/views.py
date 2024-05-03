from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Customer_Caf, UploadDocument,Photograph_upload
from .serializers import Customer_CafSerializer,UploadDocumentSerializer,Photograph_uploadSerializer
from applicants.models import Applicants
from utils import response_data, save_comment
from django.shortcuts import get_object_or_404



class Customer_CafAPIView(APIView):
    serializer_class = Customer_CafSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Customer_Caf.objects.order_by('-created_at')

    def get_caf_detail(self, pk):
        try:
            return self.queryset.get(caf_id=pk)
        except Customer_Caf.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        caf_id = data.get('data')

        if caf_id and Customer_Caf.objects.filter(caf_id=caf_id).exists():
            caf_obj = Customer_Caf.objects.get(caf_id=caf_id)
            serializer = self.serializer_class(caf_obj, data=data)
        else:
            application_id = data.get('applicant_id')
            if Applicants.objects.filter(application_id=application_id).exists():
                applicant = Applicants.objects.get(application_id=application_id)
                data['applicant'] = applicant.pk
            # else:
            #     return Response(response_data(True, "Applicant not found"), status=status.HTTP_400_BAD_REQUEST)

            comment = save_comment(data.get('comment'))
            if comment:
                data['comment'] = comment.pk

            serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(False, "caf created successfully", serializer.data), status=status.HTTP_201_CREATED)
        else:
            return Response(response_data(True, "Something went wrong", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request):
    #     try:
    #         caf_id = request.query_params.get('caf_id')
    #         application_id = request.query_params.get('application_id')
    #         # caf_obj = None
    #         if caf_id:
    #             if self.queryset.filter(caf_id=caf_id).exists():
    #                 caf_obj = self.queryset.get(caf_id=caf_id)
    #             else:
    #                 return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
    #         elif application_id:
    #             if self.queryset.filter(applicant__application_id=application_id).exists():
    #                 caf_obj = self.queryset.get(applicant__application_id=application_id)
    #             else:
    #                 return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
    #         else:
    #             return Response(response_data(True, "CAF ID not provided"), status=status.HTTP_400_BAD_REQUEST)
            
    #         serializer = self.serializer_class(caf_obj)
    #         return Response(response_data(False, "Collateral details found", serializer.data), status=status.HTTP_200_OK)
    #     except Exception as e:
    #         return Response(response_data(True, str(e)), status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
            try:
                caf_id = request.query_params.get('caf_id')
                application_id = request.query_params.get('application_id')
                if caf_id:
                    caf_obj = Customer_Caf.objects.get(caf_id=caf_id)
                    serializer = self.serializer_class(caf_obj)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                
                elif application_id:
                    if self.queryset.filter(applicant__application_id=application_id).exists():
                        caf_obj = self.queryset.get(applicant__application_id=application_id)
                    else:
                        return Response(response_data(True, "Collateral not found"), status=status.HTTP_404_NOT_FOUND)
                else:
                    queryset = Customer_Caf.objects.all()
                    serializer = self.serializer_class(queryset, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            except Customer_Caf.DoesNotExist:
                return Response({"error": True, "message": "Customer CAF not found"}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response({"error": True, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, caf_id):
        caf_details = self.get_caf_detail(caf_id)
        if caf_details:
            serializer = self.serializer_class(caf_details, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(False, "CAF detail updated successfully", serializer.data), status=status.HTTP_200_OK)
            else:
                return Response(response_data(True, "Something went wrong", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(response_data(True, "CAF detail not found"), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, caf_id):
        caf_details = self.get_caf_detail(caf_id)
        if caf_details:
            caf_details.delete()
            return Response(response_data(False, "CAF detail deleted"), status=status.HTTP_200_OK)
        else:
            return Response(response_data(True, "CAF detail not found"), status=status.HTTP_404_NOT_FOUND)






class UploadDocumentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadDocumentSerializer
    queryset = UploadDocument.objects.all()

    def get_object(self, pk):
        try:
            return self.queryset.get(pk=pk)
        except UploadDocument.DoesNotExist:
            return None

    def get(self, request, pk=None):
        if pk:
            document = self.get_object(pk)
            if document:
                serializer = self.serializer_class(document)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(response_data(True, "Document not found"), status=status.HTTP_404_NOT_FOUND)

        documents = UploadDocument.objects.all()
        serializer = self.serializer_class(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(response_data(False, "Document uploaded successfully", serializer.data), status=status.HTTP_201_CREATED)
        return Response(response_data(True, "Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        document = self.get_object(pk)
        if document:
            serializer = self.serializer_class(document, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(response_data(False, "Document updated successfully", serializer.data), status=status.HTTP_200_OK)
            return Response(response_data(True, "Invalid data", serializer.errors), status=status.HTTP_400_BAD_REQUEST)
        return Response(response_data(True, "Document not found"), status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        document = self.get_object(pk)
        if document:
            document.delete()
            return Response(response_data(False, "Document deleted successfully"), status=status.HTTP_200_OK)
        return Response(response_data(True, "Document not found"), status=status.HTTP_404_NOT_FOUND)
    





class PhotographUploadAPIView(APIView):
    serializer_class = Photograph_uploadSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Photograph_upload.objects.all()

    def get_photograph_detail(self, pk):
        try:
            return self.queryset.get(photo_id=pk)
        except Photograph_upload.DoesNotExist:
            return None
    
    def post(self, request):
        data = request.data.copy()
        photo_id = data.get('data')

        if photo_id and Photograph_upload.objects.filter(photo_id=photo_id).exists():
            photo_obj = Customer_Caf.objects.get(photo_id=photo_id)
            serializer = self.serializer_class(photo_obj, data=data)
        else:
            application_id = data.get('applicant_id')
            if Applicants.objects.filter(application_id=application_id).exists():
                applicant = Applicants.objects.get(application_id=application_id)
                data['applicant'] = applicant.pk
            # else:
            #     return Response(response_data(True, "Applicant not found"), status=status.HTTP_400_BAD_REQUEST)

            comment = save_comment(data.get('comment'))
            if comment:
                data['comment'] = comment.pk

            serializer = self.serializer_class(data=data)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        photographs = self.queryset.all()
        applicant_id = request.query_params.get('applicant_id')
        if applicant_id:
            photographs = photographs.filter(applicant=applicant_id)

        serializer = self.serializer_class(photographs, many=True)
        return Response(serializer.data)

    def put(self, request, pk):
        photograph = get_object_or_404(Photograph_upload, pk=pk)
        serializer = self.serializer_class(photograph, data=request.data)
        if serializer.is_valid():
            applicant_id = request.data.get('applicant')
            if photograph.applicant.pk != applicant_id:
                return Response({"error": True, "message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        photograph = get_object_or_404(Photograph_upload, pk=pk)
        applicant_id = request.data.get('applicant')
        if photograph.applicant.pk != applicant_id:
            return Response({"error": True, "message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        photograph.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
