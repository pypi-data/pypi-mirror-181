'''
# Polycons

A framework for building polymorphic [constructs](https://github.com/aws/constructs).
Think of polycons like dependency injection for constructs.

polycons can be used with any CDK framework, including [AWS CDK](https://github.com/aws/aws-cdk), [cdktf](https://github.com/hashicorp/terraform-cdk), and [cdk8s](https://github.com/cdk8s-team/cdk8s).

## 🚀 Getting started

Polycons can be used just like ordinary constructs:

```python
import { Dog } from "@acme/shared-polycons";
import { Construct } from "constructs";

class Pets extends Construct {
  constructor(scope: Construct, id: string) {
    super(scope, id);

    // this is a polycon!
    new Dog(this, "Dog", { treats: 5 });

    // like ordinary constructs, polycons can have methods, properties, etc.
    dog.giveBone();
  }
}
```

This `Pets` construct contains a `Dog` from a library of polycons.
The dog could have multiple implementations -- a `Labrador`, a `Terrier`, or your own implementation.

To use polycons in an application, you need to register a factory that specifies how to turn polycons into concrete constructs.
In the example below, a `PetFactory` is used, which has been defined to resolve each `Dog` in the construct tree into a `Labrador`.
By registering it to the root `App` construct, each `Dog` in the construct tree will be created as a `Labrador`.

```python
import { App } from "<cdk-framework>";
import { PetFactory } from "@acme/shared-polycons";
import { Polycons } from "polycons";

const app = new App();
Polycons.register(app, new PetFactory());
new Pets(app, "MyPets");
```

Check out the usage guide for more details about how to create your own polycons and polycon factories.

## 📖 Documentation

Click [here](./API.md) to visit the polycons API reference.

### 🏭 Polycon factories

A polycon factory is a class that implements the `IPolyconFactory` interface, which has a single `resolve()` method.
This method accepts a `type` and a list of construct arguments, and returns a concrete construct. For example:

```python
import { DOG_TYPE, CAT_TYPE, Labrador, Kitten } from "@acme/shared-polycons";

class PetFactory implements IPolyconFactory {
  public resolve(
    type: string,
    scope: Construct,
    id: string,
    ...args: any[]
  ): Construct {
    switch (type) {
      case DOG_TYPE:
        return new Labrador(scope, id, ...args);
      case CAT_TYPE:
        return new Kitten(scope, id, ...args);
      default:
        throw new Error(`Type "${type}" not implemented.`);
    }
  }
}
```

In the above example, `DOG_TYPE` and `CAT_TYPE` are unique string constants associated with the respective polycons.

By customizing the `resolve()` method, it's possible to change construct IDs, override properties, or even make factories that call other factories.

### ✍️ Creating polycons

You can define a new polycon by creating a class that returns a new Polycon instance in its constructor.
Each polycon must be associated with a unique identifying string.

```python
import { Constructs } from "constructs";
import { Polycons } from "polycons";

export interface DogProps {
  readonly name?: string;
  readonly treats?: number;
}

// make sure your polycon has a globally unique name!
export const DOG_TYPE = "@acme/shared-polycons.Dog";

export class Dog extends Construct {
  constructor(scope: Construct, id: string, props: DogProps) {
    super(null as any, id); // (1)
    return Polycons.newInstance(DOG_TYPE, scope, id, props) as Dog;
  }
}
```

The `Dog` class definition serves as an empty shell, or placeholder -- only when a user calls `new Dog()`, a real construct will be returned.

In the constructor of `Dog`, a null value MUST be passed as the first argument to `super()` (1).
This is because actually two constructs are made by the constructor, and the first one should be thrown away (and not be added to the construct tree).

Concrete implementations of a polycon can be written like ordinary constructs:

```python
export class Labrador extends Construct {
  public readonly name: string;
  private readonly treats: number;
  constructor(scope: Construct, id: string, props: DogProps) {
    super(scope, id);
    this.name = props.name;
    this.treats = props.treats;
  }
  public toString() {
    return `Labrador with ${this.treats} treats.`;
  }
}
```

### 🤝 Sharing behavior

Oftentimes, you may want all polycons to share some properties or methods.

You can achieve this by defining a base class, and having the polycon extend the base class:

```python
export interface DogProps {
  readonly name?: string;
  readonly treats?: number;
}

export const DOG_TYPE = "@acme/shared-polycons.Dog";

// This is the polycon.
export class Dog extends DogBase {
  constructor(scope: Construct, id: string, props: DogProps) {
    super(null as any, id, props); // [1]
    return Polycons.newInstance(DOG_TYPE, scope, id, props) as Dog;
  }
  public toString() {
    throw new Error("Method not implemented"); // [2]
  }
}

// This is the base class.
export abstract class DogBase extends Construct {
  public readonly species = "Canis familiaris";
  public readonly treats: number;
  constructor(scope: Construct, id: string, props: DogProps) {
    super(scope, id);

    // [3]
    if (!scope) {
      this.treats = 0;
      return;
    }

    this.treats = props.treats;
  }
  public abstract toString(): string;
}
```

Please take note:

1. In the constructor of the polycon (`Dog`), a null value MUST be passed as the first argument to `super()`.
2. Since the `Dog` class is just an empty shell, and does not get returned to the user, any methods required by the `abstract` base class can be left unimplemented.
3. In the constructor of the base class (`DogBase`), the constructor should have no side effects or mutations when an empty `scope` is passed (otherwise, side effects may occur multiple times). In the example above, we set dummy values when the scope is empty (`this.treats = 0;`) and return early.

When a polycon has a base class, every polycon implementation should extend it instead of extending `Construct`:

```python
export class Labrador extends DogBase {
  public readonly name: string;
  constructor(scope: Construct, id: string, props: DogProps) {
    super(scope, id, props);
    this.name = props.name;
  }
  public toString() {
    return `Labrador with ${this.treats} treats.`;
  }
}
```

## ✋ Contributing

We welcome community contributions and pull requests. See [CONTRIBUTING.md](./CONTRIBUTING.md) for information on how to set up a development environment and submit code on GitHub.

## ⚖️ License

This library is licensed under the Apache-2.0 license.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="polycons.IPolyconFactory")
class IPolyconFactory(typing_extensions.Protocol):
    '''A factory that determines how to turn polycons into concrete constructs.'''

    @jsii.member(jsii_name="resolve")
    def resolve(
        self,
        type: builtins.str,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *args: typing.Any,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Resolve the parameters needed for creating a specific polycon into a concrete construct.

        :param type: The type identifier.
        :param scope: The construct scope.
        :param id: The construct identifier.
        :param args: The rest of the construct's arguments.

        :return: The resolved construct
        '''
        ...


class _IPolyconFactoryProxy:
    '''A factory that determines how to turn polycons into concrete constructs.'''

    __jsii_type__: typing.ClassVar[str] = "polycons.IPolyconFactory"

    @jsii.member(jsii_name="resolve")
    def resolve(
        self,
        type: builtins.str,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *args: typing.Any,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Resolve the parameters needed for creating a specific polycon into a concrete construct.

        :param type: The type identifier.
        :param scope: The construct scope.
        :param id: The construct identifier.
        :param args: The rest of the construct's arguments.

        :return: The resolved construct
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__90f4d2552896a4f923cac6de084ddd67d53aac3350187917044faab13e4a2f8d)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument args", value=args, expected_type=typing.Tuple[type_hints["args"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.invoke(self, "resolve", [type, scope, id, *args]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPolyconFactory).__jsii_proxy_class__ = lambda : _IPolyconFactoryProxy


class Polycons(metaclass=jsii.JSIIMeta, jsii_type="polycons.Polycons"):
    '''Functions for resolving polycons (polymorphic constructs) into specific constructs.'''

    @jsii.member(jsii_name="newInstance")
    @builtins.classmethod
    def new_instance(
        cls,
        type: builtins.str,
        scope: _constructs_77d1e7e8.IConstruct,
        id: builtins.str,
        *args: typing.Any,
    ) -> _constructs_77d1e7e8.IConstruct:
        '''Creates a new instance of a polycon.

        The polycon is resolved using the
        polycon factory that is registered nearest to it in the tree.

        For example, if a construct tree has Root -> Parent -> MyPoly, and FactoryA
        is registered to Root while FactoryB is registered to Parent, then
        FactoryB will be used to resolve MyPoly.

        :param type: The type identifier.
        :param scope: The construct scope.
        :param id: The construct identifier.
        :param args: The rest of the construct's arguments.

        :return: The resolved construct
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf1113efd5d7a434e4bf7b5a1995b791e33a8a793d959a40ec4054af74d7c09)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument args", value=args, expected_type=typing.Tuple[type_hints["args"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(_constructs_77d1e7e8.IConstruct, jsii.sinvoke(cls, "newInstance", [type, scope, id, *args]))

    @jsii.member(jsii_name="register")
    @builtins.classmethod
    def register(
        cls,
        scope: _constructs_77d1e7e8.IConstruct,
        factory: IPolyconFactory,
    ) -> None:
        '''Adds a factory at given scope.

        This factory will be used for resolving
        polycons under this scope into constructs.

        :param scope: -
        :param factory: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__54376b14701c7bae7c12ddcb437987620ab48b309f3d48b57e8ce51b2fa25e5d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument factory", value=factory, expected_type=type_hints["factory"])
        return typing.cast(None, jsii.sinvoke(cls, "register", [scope, factory]))


__all__ = [
    "IPolyconFactory",
    "Polycons",
]

publication.publish()

def _typecheckingstub__90f4d2552896a4f923cac6de084ddd67d53aac3350187917044faab13e4a2f8d(
    type: builtins.str,
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *args: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf1113efd5d7a434e4bf7b5a1995b791e33a8a793d959a40ec4054af74d7c09(
    type: builtins.str,
    scope: _constructs_77d1e7e8.IConstruct,
    id: builtins.str,
    *args: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54376b14701c7bae7c12ddcb437987620ab48b309f3d48b57e8ce51b2fa25e5d(
    scope: _constructs_77d1e7e8.IConstruct,
    factory: IPolyconFactory,
) -> None:
    """Type checking stubs"""
    pass
