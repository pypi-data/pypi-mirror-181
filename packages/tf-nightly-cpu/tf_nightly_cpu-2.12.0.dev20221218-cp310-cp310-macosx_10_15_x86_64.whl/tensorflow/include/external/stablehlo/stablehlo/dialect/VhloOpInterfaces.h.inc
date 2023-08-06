/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Declarations                                                     *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

class VersionedInterface;
namespace detail {
struct VersionedInterfaceInterfaceTraits {
  struct Concept {
    mlir::vhlo::Version (*getMinVersion)(const Concept *impl, ::mlir::Operation *);
    mlir::vhlo::Version (*getMaxVersion)(const Concept *impl, ::mlir::Operation *);
  };
  template<typename ConcreteOp>
  class Model : public Concept {
  public:
    using Interface = VersionedInterface;
    Model() : Concept{getMinVersion, getMaxVersion} {}

    static inline mlir::vhlo::Version getMinVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline mlir::vhlo::Version getMaxVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteOp>
  class FallbackModel : public Concept {
  public:
    using Interface = VersionedInterface;
    FallbackModel() : Concept{getMinVersion, getMaxVersion} {}

    static inline mlir::vhlo::Version getMinVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
    static inline mlir::vhlo::Version getMaxVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val);
  };
  template<typename ConcreteModel, typename ConcreteOp>
  class ExternalModel : public FallbackModel<ConcreteModel> {
  public:
    using ConcreteEntity = ConcreteOp;
  };
};template <typename ConcreteOp>
struct VersionedInterfaceTrait;

} // namespace detail
class VersionedInterface : public ::mlir::OpInterface<VersionedInterface, detail::VersionedInterfaceInterfaceTraits> {
public:
  using ::mlir::OpInterface<VersionedInterface, detail::VersionedInterfaceInterfaceTraits>::OpInterface;
  template <typename ConcreteOp>
  struct Trait : public detail::VersionedInterfaceTrait<ConcreteOp> {};
  /// Returns the minimum version an op is supported in.
  mlir::vhlo::Version getMinVersion();
  /// Returns the maximum verison an op is supported in.
  mlir::vhlo::Version getMaxVersion();
};
namespace detail {
  template <typename ConcreteOp>
  struct VersionedInterfaceTrait : public ::mlir::OpInterface<VersionedInterface, detail::VersionedInterfaceInterfaceTraits>::Trait<ConcreteOp> {
  };
}// namespace detail
template<typename ConcreteOp>
mlir::vhlo::Version detail::VersionedInterfaceInterfaceTraits::Model<ConcreteOp>::getMinVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getMinVersion();
}
template<typename ConcreteOp>
mlir::vhlo::Version detail::VersionedInterfaceInterfaceTraits::Model<ConcreteOp>::getMaxVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return (llvm::cast<ConcreteOp>(tablegen_opaque_val)).getMaxVersion();
}
template<typename ConcreteOp>
mlir::vhlo::Version detail::VersionedInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getMinVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getMinVersion(tablegen_opaque_val);
}
template<typename ConcreteOp>
mlir::vhlo::Version detail::VersionedInterfaceInterfaceTraits::FallbackModel<ConcreteOp>::getMaxVersion(const Concept *impl, ::mlir::Operation *tablegen_opaque_val) {
  return static_cast<const ConcreteOp *>(impl)->getMaxVersion(tablegen_opaque_val);
}
