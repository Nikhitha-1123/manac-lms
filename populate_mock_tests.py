import os
import django
import json

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manac_lms.settings')
django.setup()

from lms.models import MockTest

# Sample mock tests data
mock_tests_data = [
    {
        'title': 'Aptitude Series A',
        'description': 'Test your quantitative aptitude skills',
        'topic': 'Aptitude',
        'total_marks': 10,
        'duration_minutes': 30,
        'questions': [
            {
                'question': 'What is 15% of 200?',
                'options': ['20', '25', '30', '35'],
                'correct': '30'
            },
            {
                'question': 'If 3 apples cost $6, how much do 9 apples cost?',
                'options': ['$12', '$18', '$24', '$30'],
                'correct': '$18'
            },
            {
                'question': 'What is the next number in the sequence: 2, 4, 8, 16, ...?',
                'options': ['24', '32', '28', '20'],
                'correct': '32'
            },
            {
                'question': 'A train travels 60 km in 1 hour. How far will it travel in 2.5 hours?',
                'options': ['120 km', '150 km', '140 km', '130 km'],
                'correct': '150 km'
            },
            {
                'question': 'What is the square root of 144?',
                'options': ['10', '11', '12', '13'],
                'correct': '12'
            },
            {
                'question': 'If x + 5 = 12, what is x?',
                'options': ['5', '6', '7', '8'],
                'correct': '7'
            },
            {
                'question': 'What is 40% of 250?',
                'options': ['80', '90', '100', '110'],
                'correct': '100'
            },
            {
                'question': 'A rectangle has length 8 cm and width 5 cm. What is its area?',
                'options': ['35 cm²', '40 cm²', '45 cm²', '50 cm²'],
                'correct': '40 cm²'
            },
            {
                'question': 'What is 7 multiplied by 9?',
                'options': ['54', '56', '58', '63'],
                'correct': '63'
            },
            {
                'question': 'If a box contains 24 chocolates and you eat 6, how many are left?',
                'options': ['16', '18', '20', '22'],
                'correct': '18'
            }
        ]
    },
    {
        'title': 'Reasoning Test',
        'description': 'Test your logical reasoning abilities',
        'topic': 'Reasoning',
        'total_marks': 10,
        'duration_minutes': 25,
        'questions': [
            {
                'question': 'Which word does not belong: Apple, Banana, Carrot, Orange?',
                'options': ['Apple', 'Banana', 'Carrot', 'Orange'],
                'correct': 'Carrot'
            },
            {
                'question': 'If all roses are flowers and some flowers fade quickly, can we conclude that some roses fade quickly?',
                'options': ['Yes', 'No', 'Maybe', 'Not enough information'],
                'correct': 'No'
            },
            {
                'question': 'What comes next: A, C, E, G, ...?',
                'options': ['H', 'I', 'J', 'K'],
                'correct': 'I'
            },
            {
                'question': 'Find the odd one out: Square, Circle, Triangle, Rectangle',
                'options': ['Square', 'Circle', 'Triangle', 'Rectangle'],
                'correct': 'Circle'
            },
            {
                'question': 'If P means +, Q means -, R means ×, S means ÷, what is 8 R 2 Q 3 S 2?',
                'options': ['10', '12', '14', '16'],
                'correct': '14'
            },
            {
                'question': 'Which number is missing: 1, 4, 9, 16, 25, ...?',
                'options': ['30', '36', '42', '49'],
                'correct': '36'
            },
            {
                'question': 'All cats are mammals. Some mammals are pets. Therefore:',
                'options': ['All cats are pets', 'Some cats are pets', 'No cats are pets', 'Some pets are cats'],
                'correct': 'Some cats are pets'
            },
            {
                'question': 'What is the opposite of "ascend"?',
                'options': ['Descend', 'Climb', 'Rise', 'Elevate'],
                'correct': 'Descend'
            },
            {
                'question': 'If you rearrange the letters "LISTEN", you get:',
                'options': ['SILENT', 'TILENS', 'LITSEN', 'SILNET'],
                'correct': 'SILENT'
            },
            {
                'question': 'Which shape can be folded into a cube?',
                'options': ['Square', 'Circle', 'Triangle', 'Hexagon'],
                'correct': 'Square'
            }
        ]
    },
    {
        'title': 'React Technical Assessment',
        'description': 'Test your React.js knowledge',
        'topic': 'React',
        'total_marks': 10,
        'duration_minutes': 40,
        'questions': [
            {
                'question': 'What is JSX?',
                'options': ['A JavaScript library', 'A syntax extension for JavaScript', 'A CSS preprocessor', 'A database'],
                'correct': 'A syntax extension for JavaScript'
            },
            {
                'question': 'What hook is used to manage state in functional components?',
                'options': ['useEffect', 'useState', 'useContext', 'useReducer'],
                'correct': 'useState'
            },
            {
                'question': 'What does the useEffect hook do?',
                'options': ['Manages component state', 'Handles side effects', 'Creates context', 'Manages routing'],
                'correct': 'Handles side effects'
            },
            {
                'question': 'How do you pass data from parent to child component?',
                'options': ['Using state', 'Using props', 'Using context', 'Using refs'],
                'correct': 'Using props'
            },
            {
                'question': 'What is the virtual DOM?',
                'options': ['A copy of the real DOM', 'A JavaScript object representation of the DOM', 'A CSS framework', 'A database'],
                'correct': 'A JavaScript object representation of the DOM'
            },
            {
                'question': 'Which method is used to update state in class components?',
                'options': ['setState', 'updateState', 'changeState', 'modifyState'],
                'correct': 'setState'
            },
            {
                'question': 'What is the purpose of keys in React lists?',
                'options': ['To style list items', 'To identify which items have changed', 'To sort the list', 'To filter the list'],
                'correct': 'To identify which items have changed'
            },
            {
                'question': 'Which lifecycle method is called after a component is rendered?',
                'options': ['componentWillMount', 'componentDidMount', 'componentWillUpdate', 'componentDidUpdate'],
                'correct': 'componentDidMount'
            },
            {
                'question': 'What is Redux used for?',
                'options': ['Styling components', 'Managing application state', 'Routing', 'HTTP requests'],
                'correct': 'Managing application state'
            },
            {
                'question': 'How do you handle forms in React?',
                'options': ['Using controlled components', 'Using uncontrolled components', 'Both A and B', 'Neither'],
                'correct': 'Both A and B'
            }
        ]
    },
    {
        'title': 'JavaScript Fundamentals',
        'description': 'Test your JavaScript knowledge',
        'topic': 'JavaScript',
        'total_marks': 10,
        'duration_minutes': 35,
        'questions': [
            {
                'question': 'What is the output of typeof null?',
                'options': ['null', 'undefined', 'object', 'boolean'],
                'correct': 'object'
            },
            {
                'question': 'Which keyword is used to declare a variable in JavaScript?',
                'options': ['var', 'let', 'const', 'All of the above'],
                'correct': 'All of the above'
            },
            {
                'question': 'What does the === operator do?',
                'options': ['Assigns a value', 'Compares values and types', 'Compares values only', 'Creates an object'],
                'correct': 'Compares values and types'
            },
            {
                'question': 'Which method adds an element to the end of an array?',
                'options': ['push', 'pop', 'shift', 'unshift'],
                'correct': 'push'
            },
            {
                'question': 'What is a closure in JavaScript?',
                'options': ['A way to close a function', 'A function that has access to its outer scope', 'A type of loop', 'A DOM element'],
                'correct': 'A function that has access to its outer scope'
            },
            {
                'question': 'Which statement is used to handle exceptions?',
                'options': ['try...catch', 'if...else', 'for...in', 'switch'],
                'correct': 'try...catch'
            },
            {
                'question': 'What does the map() method do?',
                'options': ['Creates a new array with results of calling a function', 'Modifies the original array', 'Sorts the array', 'Filters the array'],
                'correct': 'Creates a new array with results of calling a function'
            },
            {
                'question': 'Which object represents the browser window?',
                'options': ['document', 'window', 'navigator', 'location'],
                'correct': 'window'
            },
            {
                'question': 'What is the purpose of the setTimeout function?',
                'options': ['To create a loop', 'To delay execution of code', 'To stop code execution', 'To create an interval'],
                'correct': 'To delay execution of code'
            },
            {
                'question': 'Which keyword is used to define a class?',
                'options': ['function', 'class', 'object', 'var'],
                'correct': 'class'
            }
        ]
    },
    {
        'title': 'Data Structures & Algorithms',
        'description': 'Test your DSA knowledge',
        'topic': 'DSA',
        'total_marks': 10,
        'duration_minutes': 45,
        'questions': [
            {
                'question': 'What is the time complexity of binary search?',
                'options': ['O(n)', 'O(log n)', 'O(n²)', 'O(1)'],
                'correct': 'O(log n)'
            },
            {
                'question': 'Which data structure uses LIFO?',
                'options': ['Queue', 'Stack', 'Array', 'Linked List'],
                'correct': 'Stack'
            },
            {
                'question': 'What is a balanced binary tree?',
                'options': ['A tree with equal left and right subtrees', 'A tree where height difference is at most 1', 'A complete binary tree', 'A full binary tree'],
                'correct': 'A tree where height difference is at most 1'
            },
            {
                'question': 'Which sorting algorithm has the best average case?',
                'options': ['Bubble Sort', 'Quick Sort', 'Insertion Sort', 'Selection Sort'],
                'correct': 'Quick Sort'
            },
            {
                'question': 'What is the space complexity of merge sort?',
                'options': ['O(1)', 'O(log n)', 'O(n)', 'O(n log n)'],
                'correct': 'O(n)'
            },
            {
                'question': 'Which traversal visits the root first?',
                'options': ['Inorder', 'Preorder', 'Postorder', 'Level order'],
                'correct': 'Preorder'
            },
            {
                'question': 'What is a hash table?',
                'options': ['A tree structure', 'A data structure that maps keys to values', 'A sorting algorithm', 'A graph'],
                'correct': 'A data structure that maps keys to values'
            },
            {
                'question': 'Which algorithm finds the shortest path in a graph?',
                'options': ['DFS', 'BFS', 'Dijkstra', 'Binary Search'],
                'correct': 'Dijkstra'
            },
            {
                'question': 'What is the worst case time complexity of quicksort?',
                'options': ['O(n log n)', 'O(n²)', 'O(n)', 'O(log n)'],
                'correct': 'O(n²)'
            },
            {
                'question': 'Which data structure is used for breadth-first search?',
                'options': ['Stack', 'Queue', 'Array', 'Linked List'],
                'correct': 'Queue'
            }
        ]
    }
]

def create_mock_tests():
    for test_data in mock_tests_data:
        mock_test, created = MockTest.objects.get_or_create(
            title=test_data['title'],
            defaults={
                'description': test_data['description'],
                'topic': test_data['topic'],
                'total_marks': test_data['total_marks'],
                'duration_minutes': test_data['duration_minutes'],
                'questions': test_data['questions'],
                'is_active': True
            }
        )
        pass

if __name__ == '__main__':
    create_mock_tests()
