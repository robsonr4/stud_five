python manage.py graph_models -a > output.dot
dot -Tpdf output.dot -o output.pdf