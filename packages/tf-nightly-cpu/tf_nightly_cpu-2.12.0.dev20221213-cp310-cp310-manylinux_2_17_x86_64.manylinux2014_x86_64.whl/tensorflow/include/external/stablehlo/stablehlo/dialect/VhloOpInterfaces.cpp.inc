/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Interface Definitions                                                      *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

/// Returns the minimum version an op is supported in.
mlir::vhlo::Version VersionedInterface::getMinVersion() {
      return getImpl()->getMinVersion(getImpl(), getOperation());
  }
/// Returns the maximum verison an op is supported in.
mlir::vhlo::Version VersionedInterface::getMaxVersion() {
      return getImpl()->getMaxVersion(getImpl(), getOperation());
  }
