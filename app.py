Administración de Datos
Subir nuevo archivo CSV

No file chosen
Drag and drop file here
Limit 200MB per file • CSV
UnicodeDecodeError: This app has encountered an error. The original error message is redacted to prevent data leaks. Full error details have been recorded in the logs (if you're on Streamlit Cloud, click on 'Manage app' in the lower right of your app).
Traceback:
File "/mount/src/tusiderca/app.py", line 79, in <module>
    df = pd.read_csv(DATA_FILE)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py", line 1026, in read_csv
    return _read(filepath_or_buffer, kwds)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py", line 620, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py", line 1620, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/io/parsers/readers.py", line 1898, in _make_engine
    return mapping[engine](f, **self.options)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
File "/home/adminuser/venv/lib/python3.13/site-packages/pandas/io/parsers/c_parser_wrapper.py", line 93, in __init__
    self._reader = parsers.TextReader(src, **kwds)
                   ~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
File "pandas/_libs/parsers.pyx", line 574, in pandas._libs.parsers.TextReader.__cinit__
File "pandas/_libs/parsers.pyx", line 663, in pandas._libs.parsers.TextReader._get_header
File "pandas/_libs/parsers.pyx", line 874, in pandas._libs.parsers.TextReader._tokenize_rows
File "pandas/_libs/parsers.pyx", line 891, in pandas._libs.parsers.TextReader._check_tokenize_status
File "pandas/_libs/parsers.pyx", line 2053, in pandas._libs.parsers.raise_parser_error
File "<frozen codecs>", line 325, in decode
