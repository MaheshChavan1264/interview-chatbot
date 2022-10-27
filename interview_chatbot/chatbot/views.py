import threading
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.http import HttpResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
import cv2
from django.views.decorators import gzip
import warnings
import PyPDF2

warnings.filterwarnings('ignore')
import docx2txt
from pdf2docx import Converter

from .models import Student


# Create your views here.

def index(request):
    return render(request, 'index.html')


def registration_page(request):
    return render(request, 'registration.html')


def register(request):
    name = request.POST.get('student_name')
    email = request.POST.get('email')
    college = request.POST.get('college')
    cgpa = request.POST.get('cgpa')
    resume = request.FILES.get('resume')

    student = Student()
    student.student_name = name
    student.student_email = email
    student.student_college = college
    student.student_cgpa = cgpa
    student.student_resume = resume
    student.save()
    student1 = Student.objects.get(student_email=email)
    resume_result = resume_screening(student1.student_resume, student1.student_email)
    print('Resume Matches by: ' + resume_result + '%')
    student1.student_resume_result = resume_result
    context = {'student': student1}
    return render(request, 'interview.html', context)


def resume_screening(path, email):
    docx_file = 'media/' + email + '_resume.docx'
    cv = Converter(path)
    cv.convert(docx_file)
    cv.close()
    job_description = docx2txt.process('media/sample_description.docx')
    resume = docx2txt.process('media/' + email + '_resume.docx')
    content = [job_description, resume]
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(content)
    mat = cosine_similarity(count_matrix)
    result = '{0:.2f}'.format(mat[1][0] * 100) + '%'
    # result = str(result) + '%'
    print('Resume Matches by: ' + result)
    return result


@gzip.gzip_page
def video_feed(request):
    try:
        cam = VideoCapture()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        pass
    return render(request, 'interview.html')


def interview(request, student_email):
    # email = request
    print(request)
    print(student_email)
    student = Student.objects.get(student_email=student_email)
    context = {'student': student}
    return render(request, 'video.html', context)


class VideoCapture(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        img = self.frame
        _, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
