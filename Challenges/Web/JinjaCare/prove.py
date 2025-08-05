class ExampleClass:
    def __init__(self, name):
        self.name = name
        print(f"Creating instance: {name}")
    
    def regular_method(self):
        return f"Hello from {self.name}"

# สร้าง instance
obj = ExampleClass("TestObject")

# ===== INTROSPECTION EXAMPLES =====

print("=== 1. Basic Object Structure ===")
print(f"obj.__class__: {obj.__class__}")
print(f"obj.__dict__: {obj.__dict__}")
print(f"obj.__module__: {obj.__module__}")

print("\n=== 2. Method และ Function Structure ===")
# เข้าถึง method
method = obj.regular_method
print(f"method.__self__: {method.__self__}")
print(f"method.__func__: {method.__func__}")

# เข้าถึง function ผ่าน __init__
init_method = obj.__init__
print(f"init_method.__globals__.keys(): {list(init_method.__globals__.keys())[:5]}...")

print("\n=== 3. Built-ins Access ===")
# วิธีการเข้าถึง builtins
print(f"__builtins__ type: {type(__builtins__)}")
if hasattr(__builtins__, 'keys'):
    print(f"Available built-ins: {list(__builtins__.keys())[:10]}...")
else:
    print(f"Built-in functions: {dir(__builtins__)[:10]}...")

print("\n=== 4. Global Namespace ===")
# เข้าถึง globals ผ่าน function
def sample_function():
    return "sample"

print(f"sample_function.__globals__.keys(): {list(sample_function.__globals__.keys())}")

print("\n=== 5. Class Hierarchy ===")
print(f"obj.__class__.__bases__: {obj.__class__.__bases__}")
print(f"obj.__class__.__mro__: {obj.__class__.__mro__}")

print("\n=== 6. Dynamic Import Example ===")
# ใช้ __import__ อย่างปลอดภัย
import_func = __import__
math_module = import_func('math')
print(f"math.pi: {math_module.pi}")

print("\n=== 7. Template Injection Chain Simulation ===")
# แสดงให้เห็น chain ที่อาจถูกใช้ใน template injection
print("Chain breakdown:")
print("1. self                    -> instance object")
print("2. self.__init__           -> constructor method")  
print("3. self.__init__.__globals__-> global namespace dict")
print("4. __globals__['__builtins__'] -> built-in functions")
print("5. __builtins__.__import__  -> import function")
print("6. __import__('os')        -> os module")
print("7. os.popen('command')     -> system command execution")

# แสดง actual chain (แต่ไม่รัน os.popen เพื่อความปลอดภัย)
try:
    globals_dict = obj.__init__.__globals__
    builtins_access = globals_dict.get('__builtins__', {})
    print(f"\nActual chain verification:")
    print(f"globals_dict is dict: {isinstance(globals_dict, dict)}")
    print(f"builtins accessible: {'__import__' in dir(builtins_access)}")
except Exception as e:
    print(f"Chain access error: {e}")

print("\n=== 8. Security Note ===")
print("⚠️  Template injection attacks exploit these introspection features")
print("⚠️  Always sanitize user input in template engines")
print("⚠️  Use sandboxed environments for untrusted code")