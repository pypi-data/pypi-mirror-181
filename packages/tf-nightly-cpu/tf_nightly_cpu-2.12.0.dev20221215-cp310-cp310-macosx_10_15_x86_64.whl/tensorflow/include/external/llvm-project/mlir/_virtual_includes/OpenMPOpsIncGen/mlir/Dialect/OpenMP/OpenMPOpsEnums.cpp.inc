/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseCancellationConstructType(ClauseCancellationConstructType val) {
  switch (val) {
    case ClauseCancellationConstructType::Parallel: return "parallel";
    case ClauseCancellationConstructType::Loop: return "loop";
    case ClauseCancellationConstructType::Sections: return "sections";
    case ClauseCancellationConstructType::Taskgroup: return "taskgroup";
  }
  return "";
}

::llvm::Optional<ClauseCancellationConstructType> symbolizeClauseCancellationConstructType(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseCancellationConstructType>>(str)
      .Case("parallel", ClauseCancellationConstructType::Parallel)
      .Case("loop", ClauseCancellationConstructType::Loop)
      .Case("sections", ClauseCancellationConstructType::Sections)
      .Case("taskgroup", ClauseCancellationConstructType::Taskgroup)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseCancellationConstructType> symbolizeClauseCancellationConstructType(uint32_t value) {
  switch (value) {
  case 0: return ClauseCancellationConstructType::Parallel;
  case 1: return ClauseCancellationConstructType::Loop;
  case 2: return ClauseCancellationConstructType::Sections;
  case 3: return ClauseCancellationConstructType::Taskgroup;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseDepend(ClauseDepend val) {
  switch (val) {
    case ClauseDepend::dependsource: return "dependsource";
    case ClauseDepend::dependsink: return "dependsink";
  }
  return "";
}

::llvm::Optional<ClauseDepend> symbolizeClauseDepend(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseDepend>>(str)
      .Case("dependsource", ClauseDepend::dependsource)
      .Case("dependsink", ClauseDepend::dependsink)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseDepend> symbolizeClauseDepend(uint32_t value) {
  switch (value) {
  case 0: return ClauseDepend::dependsource;
  case 1: return ClauseDepend::dependsink;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseGrainsizeType(ClauseGrainsizeType val) {
  switch (val) {
    case ClauseGrainsizeType::Strict: return "strict";
  }
  return "";
}

::llvm::Optional<ClauseGrainsizeType> symbolizeClauseGrainsizeType(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseGrainsizeType>>(str)
      .Case("strict", ClauseGrainsizeType::Strict)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseGrainsizeType> symbolizeClauseGrainsizeType(uint32_t value) {
  switch (value) {
  case 0: return ClauseGrainsizeType::Strict;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseMemoryOrderKind(ClauseMemoryOrderKind val) {
  switch (val) {
    case ClauseMemoryOrderKind::Seq_cst: return "seq_cst";
    case ClauseMemoryOrderKind::Acq_rel: return "acq_rel";
    case ClauseMemoryOrderKind::Acquire: return "acquire";
    case ClauseMemoryOrderKind::Release: return "release";
    case ClauseMemoryOrderKind::Relaxed: return "relaxed";
  }
  return "";
}

::llvm::Optional<ClauseMemoryOrderKind> symbolizeClauseMemoryOrderKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseMemoryOrderKind>>(str)
      .Case("seq_cst", ClauseMemoryOrderKind::Seq_cst)
      .Case("acq_rel", ClauseMemoryOrderKind::Acq_rel)
      .Case("acquire", ClauseMemoryOrderKind::Acquire)
      .Case("release", ClauseMemoryOrderKind::Release)
      .Case("relaxed", ClauseMemoryOrderKind::Relaxed)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseMemoryOrderKind> symbolizeClauseMemoryOrderKind(uint32_t value) {
  switch (value) {
  case 0: return ClauseMemoryOrderKind::Seq_cst;
  case 1: return ClauseMemoryOrderKind::Acq_rel;
  case 2: return ClauseMemoryOrderKind::Acquire;
  case 3: return ClauseMemoryOrderKind::Release;
  case 4: return ClauseMemoryOrderKind::Relaxed;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseNumTasksType(ClauseNumTasksType val) {
  switch (val) {
    case ClauseNumTasksType::Strict: return "strict";
  }
  return "";
}

::llvm::Optional<ClauseNumTasksType> symbolizeClauseNumTasksType(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseNumTasksType>>(str)
      .Case("strict", ClauseNumTasksType::Strict)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseNumTasksType> symbolizeClauseNumTasksType(uint32_t value) {
  switch (value) {
  case 0: return ClauseNumTasksType::Strict;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseOrderKind(ClauseOrderKind val) {
  switch (val) {
    case ClauseOrderKind::Concurrent: return "concurrent";
  }
  return "";
}

::llvm::Optional<ClauseOrderKind> symbolizeClauseOrderKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseOrderKind>>(str)
      .Case("concurrent", ClauseOrderKind::Concurrent)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseOrderKind> symbolizeClauseOrderKind(uint32_t value) {
  switch (value) {
  case 1: return ClauseOrderKind::Concurrent;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseProcBindKind(ClauseProcBindKind val) {
  switch (val) {
    case ClauseProcBindKind::Primary: return "primary";
    case ClauseProcBindKind::Master: return "master";
    case ClauseProcBindKind::Close: return "close";
    case ClauseProcBindKind::Spread: return "spread";
  }
  return "";
}

::llvm::Optional<ClauseProcBindKind> symbolizeClauseProcBindKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseProcBindKind>>(str)
      .Case("primary", ClauseProcBindKind::Primary)
      .Case("master", ClauseProcBindKind::Master)
      .Case("close", ClauseProcBindKind::Close)
      .Case("spread", ClauseProcBindKind::Spread)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseProcBindKind> symbolizeClauseProcBindKind(uint32_t value) {
  switch (value) {
  case 0: return ClauseProcBindKind::Primary;
  case 1: return ClauseProcBindKind::Master;
  case 2: return ClauseProcBindKind::Close;
  case 3: return ClauseProcBindKind::Spread;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyClauseScheduleKind(ClauseScheduleKind val) {
  switch (val) {
    case ClauseScheduleKind::Static: return "static";
    case ClauseScheduleKind::Dynamic: return "dynamic";
    case ClauseScheduleKind::Guided: return "guided";
    case ClauseScheduleKind::Auto: return "auto";
    case ClauseScheduleKind::Runtime: return "runtime";
  }
  return "";
}

::llvm::Optional<ClauseScheduleKind> symbolizeClauseScheduleKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ClauseScheduleKind>>(str)
      .Case("static", ClauseScheduleKind::Static)
      .Case("dynamic", ClauseScheduleKind::Dynamic)
      .Case("guided", ClauseScheduleKind::Guided)
      .Case("auto", ClauseScheduleKind::Auto)
      .Case("runtime", ClauseScheduleKind::Runtime)
      .Default(::std::nullopt);
}
::llvm::Optional<ClauseScheduleKind> symbolizeClauseScheduleKind(uint32_t value) {
  switch (value) {
  case 0: return ClauseScheduleKind::Static;
  case 1: return ClauseScheduleKind::Dynamic;
  case 2: return ClauseScheduleKind::Guided;
  case 3: return ClauseScheduleKind::Auto;
  case 4: return ClauseScheduleKind::Runtime;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

namespace mlir {
namespace omp {
::llvm::StringRef stringifyScheduleModifier(ScheduleModifier val) {
  switch (val) {
    case ScheduleModifier::none: return "none";
    case ScheduleModifier::monotonic: return "monotonic";
    case ScheduleModifier::nonmonotonic: return "nonmonotonic";
    case ScheduleModifier::simd: return "simd";
  }
  return "";
}

::llvm::Optional<ScheduleModifier> symbolizeScheduleModifier(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::llvm::Optional<ScheduleModifier>>(str)
      .Case("none", ScheduleModifier::none)
      .Case("monotonic", ScheduleModifier::monotonic)
      .Case("nonmonotonic", ScheduleModifier::nonmonotonic)
      .Case("simd", ScheduleModifier::simd)
      .Default(::std::nullopt);
}
::llvm::Optional<ScheduleModifier> symbolizeScheduleModifier(uint32_t value) {
  switch (value) {
  case 0: return ScheduleModifier::none;
  case 1: return ScheduleModifier::monotonic;
  case 2: return ScheduleModifier::nonmonotonic;
  case 3: return ScheduleModifier::simd;
  default: return ::std::nullopt;
  }
}

} // namespace omp
} // namespace mlir

