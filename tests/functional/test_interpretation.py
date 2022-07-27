from smallscheme.runner import Runner

class Output(object):
    def __init__(self):
        self.buffer = []
    def write(self, string):
        self.buffer.append(string)
    def get(self):
        result = ''.join(self.buffer)
        self.buffer = []
        return result

out = Output()
runner = Runner(out)

def test_aritmetics():
    runner.run("""
        (display (+ 2 5))
        (display ", ")
        (display (* 2 4))
        (display ", ")
        (display (/ 9 3))
        (display ", ")
        (display (- 10 2 2 2 2 2))
        (newline)
    """)
    assert "7, 8, 3, 0\n" == out.get()

def test_iteration():
    runner.run("""
        (define run-10
          (lambda ()
            (define iter
              (lambda (i)
                (display i)
                (if (< i 10)
                  (begin
                    (display ", ")
                    (iter (1+ i)))
                  (newline))))
            (iter 0)))
        (run-10)
    """)
    assert "0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10\n" == out.get()

def test_scope():
    runner.run("""
        (define a 'bar)
        ((lambda ()
          (define a 'foo)
          (display a)))
        (display a)
    """)
    assert "foobar" == out.get()

def test_scope_begin():
    # begin does not creates scope
    runner.run("""
        (define a 'foo)
        (begin
          (display a)
          (define a 'bar)
          (display a))
        (display a)
    """)
    assert "foobarbar" == out.get()

def test_tail_recursion():
    runner.run("""
        (define to-1001
          (lambda ()
            (define iter
              (lambda (i)
                (cond ((= i 1001) (display i))
                      (else (iter (1+ i))))))
            (iter 0)))
        (to-1001)
    """)
    assert "1001" == out.get()

def test_closures():
    runner.run("""
        (define make-counter
          (lambda ()
            (define counter 0)
            (lambda ()
              (set! counter (1+ counter))
              counter)))

        (define counter-1 (make-counter))
        (define counter-2 (make-counter))

        (display (counter-1))
        (display (counter-2))
        (display (counter-1))
        (display (counter-2))
        (display (counter-1))
        (display (counter-2))
    """)
    assert "112233" == out.get()

def test_map_implementation():
    runner.run("""
        (define map
          (lambda (func l)
            (cond ((null? l) '())
                  (else (cons (func (car l)) (map func (cdr l)))))))

        (display (map 1+ '(1 2 3 4 5)))
    """)
    assert '(2 3 4 5 6)' == out.get()

def test_filter_implementation():
    runner.run("""
        (define filter
          (lambda (func l)
            (cond ((null? l) '())
                  ((func (car l)) (cons (car l)
                                        (filter func (cdr l))))
                  (else (filter func (cdr l))))))

        (define even?
          (lambda (number)
            (= 0 (modulo number 2))))

        (display (filter even? '(1 2 3 4 5 6 7)))
    """)
    assert '(2 4 6)' == out.get()


def test_reduce_implementation():
    runner.run("""
        (define reduce
          (lambda (func identity l)
            (cond ((null? l) identity)
                  (else (reduce func
                                (func identity (car l))
                                (cdr l))))))

        (display (reduce + 0 '(1 2 3 4 5 6 7 8 9 10)))
    """)
    assert '55' == out.get()

