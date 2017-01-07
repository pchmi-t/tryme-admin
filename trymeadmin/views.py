from jsonrpc import jsonrpc_method
from django.http import HttpResponse
from django.core import serializers
from django.forms.models import model_to_dict
from trymeadmin.models import Test, Category, Question, Answer


@jsonrpc_method('all_categories')
def all_categories(request):
    categories = Category.objects.all()
    
    categories_data = []
    for category in categories:
        category_data = model_to_dict(category)
        category_data['tests_count'] = Test.objects.filter(category__id=category.id).count()
        categories_data.append(category_data)
    return categories_data

@jsonrpc_method('tests_for_category')
def tests_for_category(request, category_id):
    try:
        category = Category.objects.get(pk=category_id)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    
    tests = Test.objects.filter(category__id=category_id)
    
    category_data = model_to_dict(category)
    
    tests_data = []
    for test in tests:
        test_data = model_to_dict(test)
        test_data['category'] = category_data
        tests_data.append(test_data)
    category_data['tests_count'] = len(tests_data)
    return tests_data

@jsonrpc_method('get_test')
def get_test(request, test_id):
    try:
        test = Test.objects.get(pk=test_id)
        
        test_data = model_to_dict(test)
        
        category_data = model_to_dict(test.category)
        category_data['tests_count'] = Test.objects.filter(category__id=test.category.id).count()
        
        questions = test.question_set.all()
        
        questions_data = []
        for question in questions:
            question_data = model_to_dict(question)
            question_data['answers'] = list(map(model_to_dict, question.answer_set.all()))
            questions_data.append(question_data)
        
        test_data['category'] = category_data
        
        return { 'description': test_data, 'questions': questions_data }
    except Test.DoesNotExist:
        raise Http404("Test does not exist")
    except Category.DoesNotExist:
        raise Http404("Category does not exist")