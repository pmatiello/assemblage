Assemblage
==========

Assemblage is an object assembler for Python programs. It can produce instances of
arbitrary classes, along which the required dependencies, effortlessly.

Installing
----------

Assemblage can be installed by <tt>easy_install</tt>:

<pre>
# easy_install assemblage
</pre>

Producing an assembler
----------------------

An assembler object, capable of instantiate registered types and and their dependencies, is easily produced:

<pre>
import assemblage

assembler = assemblage.assembler()
</pre>

Registering and instantiating types
-----------------------------------

Let <tt>lightbulb</tt> be a type defined as below:

<pre>
class lightbulb(object):
    pass
</pre>

The following line registers this type in the assembler object:

<pre>
assembler.register(lightbulb)
</pre>

And a instance of <tt>lightbulb</tt> is built by the following call:

<pre>
assembler.provide(lightbulb)
</pre>

Declaring dependencies
----------------------

Types might have dependencies. Assemblage is capable of providing these dependencies by passing them to the type constructor.

Let <tt>bedroom</tt> be a type defined as below:

<pre>
class car(object):

    def __init__(self, bed, wardrobe, lightbulb):
        self.bed = bed
        self.wardrobe = wardrobe
        self.lightbulb = lightbulb
</pre>

Instances of <tt>bedroom</tt> require instances of the types <tt>bed</tt>, <tt>wardrobe</tt> and <tt>lightbulb</tt>. These requirements, therefore, must be expressed when the <tt>bedroom</tt> type is registered in the assembler:

<pre>
assembler.register(bedroom, requires=[bed, wardrobe, lightbulb])
</pre>

Instances of the required classes will be automatically provided when an instance of <tt>bedroom</tt> is requested:

<pre>
assembler.provide(bedroom)
</pre>

Using factories
---------------

Often, an usable object cannot be built by a simple constructor call. In cases like these, a factory method can be provided to instruct the assembler on how to build the desired type.

Let <tt>trash_can</tt> be a type as defined below:

<pre>
class trash_can(object):

    def __init__(self):
        self.bag = None
    
    def set_plastic_bag(self, bag):
        self.bag = bag
</pre>

The assembler can produce instances of the <tt>trash_can</tt> class, and automatically feed them instances of <tt>plastic_bag</tt>, through the usage of a factory method:

<pre>
def make_trash_can(plastic_bag):
    trash = trash_can()
    bag = plastic_bag()
    trash.set_plastic_bag(bag)
    return trash

assembler.register(trash_can, depends=[plastic_bag], factory=make_trash_can)
</pre>

Avoiding instance sharing
-------------------------

By default, the assembler will cache every object it produces. Then, when an instance of a type is requested, the assembler will return the previously cached instance of that type, if it exists.

It's possible to have a new instance produced at every <tt>provide</tt> call by registering the type as uncacheable:

<pre>
assembler.register(plastic_bag, cacheable=False)
</pre>

Scoping
-------

It's possible to implement different scopes for the objects in an application by using different assembler objects. Still, it's convenient to have different assemblers sharing cached instances and construction rules.

Given an assembler, an child assembler can be produced:

<pre>
child_assembler = parent_assembler.spawn_child()
</pre>

The child assembler have access to all construction rules and cached instances present in the parent assembler.
