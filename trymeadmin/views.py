from jsonrpc import jsonrpc_method
from django.core import serializers
from django.forms.models import model_to_dict
from trymeadmin.models import Test, Category, Question, Answer


@jsonrpc_method('all_categories')
def all_categories(request):
  return serializers.serialize("json", Category.objects.all())

@jsonrpc_method('tests_for_category')
def tests_for_category(request, category_id):
    tests = Test.objects.filter(category__id=category_id)
    return serializers.serialize("json", tests)

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