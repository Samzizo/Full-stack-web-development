import os
import sys
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

"""Set number of questions per page
the page numbered questions will take request and selection
Marke start and end of the questions
defined the Creation application using the Test configuration None
"""

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """Set up CORS. Allow '*' for origins."""

    CORS(app, resources={'/': {'origins': '*'}})

    """Use the after_request decorator to set Access-Control-Allow
    the headers content type Authorization - allowed  different methods
    in the response headers
    """

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers', 'Content-Type, Authorization, true'
        )
        response.headers.add(
            'Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS'
        )
        response.headers.add('Access-Control-Allow-origins', '*')
        return response

    """create an endpoint
    If no category found then abort 404(Not Found)
    Response body keys: 'success', 'categories' 'total_categories'
    """

    @app.route('/categories', methods=["GET"])
    def retrive_all_categories():
        categories = Category.query.all()
        data = {}
        for category in categories:
            data[category.id] = category.type

        if len(data) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': data,
            'total_categories': len(categories)
        })

    """create an endpoint
    route that get questions, paginated (every 10 questions)
    A query about the questions
    If no questions found, abort 404
    Response body keys:
    'success', 'categories', 'current_category','total_questions'
    """

    @app.route('/questions', methods=['GET'])
    def get_questions():
        categories = Category.query.order_by(Category.type).all()
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': {
                category.id: category.type for category in categories
            },
            'current category': None
        })

    """Delete the question using a question ID"""

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'deleted': question_id,
                'questions': current_questions,
                'total_questions': len(selection)
            })
        except:
            print(sys.exc_info())
            abort(422)

    """Route that create a new question
    Response body keys:
    'success', 'created'(id of created question),
    'questions', 'total_questions'
    Inserts a new question
    """

    @app.route('/questions', methods=['POST'])
    def create_new_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)
        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))
                )
                current_questions = paginate_questions(request, selection)
                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(selection.all())
                })
            else:
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty
                )
                question.insert()
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })

        except:
            print(sys.exc_info())
            abort(422)

    """Get questions based on a search term
    Return any questions for whom the search term
    """

    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        body = request.get_json()
        search_term = body.get('searchTerm', None)
        try:
            if search_term:
                selection = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')
                ).all()
                paginated = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions':  paginated,
                    'total_questions': len(selection),
                    'current_category': None
                })

        except:
            print(sys.exc_info())
            abort(404)

    """Create a GET endpoint to get questions based on category."""

    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_by_category(id):
        category = Category.query.filter_by(id=id).one_or_none()
        if (category is None):
            abort(422)
        try:
            questions = Question.query.filter_by(
                category=category.id
            ).all()
            current_questions = paginate_questions(request, questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(questions),
                'current_category': category.type
            })
        except:
            print(sys.exc_info())
            abort(400)

    """Create a POST endpoint to get questions to play the quizz.
    take category and previous question parameters
    return a random questions within the given category
    if provided, and that is not one of the previous questions.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body['previous_questions']
            category_id = body['quiz_category']['id']
            print(previous_questions, category_id)

            if category_id == 0:
                selection = Question.query.filter(Question.id.notin_(
                    previous_questions
                )).all()
            else:
                selection = Question.query.filter(
                    Question.category == category_id, Question.id.notin_(
                        previous_questions
                    )
                ).all()

            current_questions = [question.format() for question in selection]

            if selection:
                question = current_questions[
                    random.randint(0, len(selection)-1)
                ]
            else:
                question = None
            return jsonify({
                'success': True,
                'question': question,
            })

        except:
            print(sys.exc_info())
            abort(422)

    """Error handler"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method Not Allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Internal Server Error"
        }), 500
    return app
