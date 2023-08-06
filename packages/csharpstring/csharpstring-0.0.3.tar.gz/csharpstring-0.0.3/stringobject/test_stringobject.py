from .csharpstring import instance, static


def test_instance():
	hello = instance("Hello");
	assert isinstance(hello, instance) == True;
	assert hello.ToString() == "Hello";

def test_in_append():
	hello = instance("Hello");
	world = instance("World!");
	msg = hello.Append(world);
	assert msg.ToString() == "Hello World!";

def test_in_prepend():
	hello = instance("Hello");
	world = instance("World!");
	msg = world.Prepend(hello);
	assert msg.ToString() == "Hello World!";

def test_in_indexof():
	msg = instance("Hello World!");
	letter = msg.IndexOf("H");
	assert letter == 0;

def test_in_split():
	msg = instance("Hello World!");
	parts = msg.Split(" ");
	assert len(parts) == 2;

def test_in_replace():
	msg = instance("Hello World");
	newmsg = msg.Replace("World", "Python");
	assert len(newmsg.ToString()) == 12;

def test_st_format():
	var = "Python";
	msg = static.Format("Hello from $0", var);
	assert len(msg) == 17;

""" static.Join() is used by, and therefor tested by Append, and Prepend """

def test_len():
	msg = instance("hello");
	test = len(msg);
	assert(test == 5);