/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Definitions                                                        *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_LIST
#undef GET_ATTRDEF_LIST

::mlir::sparse_tensor::SparseTensorEncodingAttr,
::mlir::sparse_tensor::StorageSpecifierKindAttr

#endif  // GET_ATTRDEF_LIST

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES

static ::mlir::OptionalParseResult generatedAttributeParser(::mlir::AsmParser &parser, ::llvm::StringRef *mnemonic, ::mlir::Type type, ::mlir::Attribute &value) {
  return ::mlir::AsmParser::KeywordSwitch<::mlir::OptionalParseResult>(parser)
    .Case(::mlir::sparse_tensor::SparseTensorEncodingAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::sparse_tensor::SparseTensorEncodingAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Case(::mlir::sparse_tensor::StorageSpecifierKindAttr::getMnemonic(), [&](llvm::StringRef, llvm::SMLoc) {
      value = ::mlir::sparse_tensor::StorageSpecifierKindAttr::parse(parser, type);
      return ::mlir::success(!!value);
    })
    .Default([&](llvm::StringRef keyword, llvm::SMLoc) {
      *mnemonic = keyword;
      return std::nullopt;
    });
}

static ::mlir::LogicalResult generatedAttributePrinter(::mlir::Attribute def, ::mlir::AsmPrinter &printer) {
  return ::llvm::TypeSwitch<::mlir::Attribute, ::mlir::LogicalResult>(def)    .Case<::mlir::sparse_tensor::SparseTensorEncodingAttr>([&](auto t) {
      printer << ::mlir::sparse_tensor::SparseTensorEncodingAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Case<::mlir::sparse_tensor::StorageSpecifierKindAttr>([&](auto t) {
      printer << ::mlir::sparse_tensor::StorageSpecifierKindAttr::getMnemonic();
t.print(printer);
      return ::mlir::success();
    })
    .Default([](auto) { return ::mlir::failure(); });
}

namespace mlir {
namespace sparse_tensor {
namespace detail {
struct SparseTensorEncodingAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType>, AffineMap, AffineMap, unsigned, unsigned>;
  SparseTensorEncodingAttrStorage(::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth) : dimLevelType(dimLevelType), dimOrdering(dimOrdering), higherOrdering(higherOrdering), pointerBitWidth(pointerBitWidth), indexBitWidth(indexBitWidth) {}

  KeyTy getAsKey() const {
    return KeyTy(dimLevelType, dimOrdering, higherOrdering, pointerBitWidth, indexBitWidth);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (dimLevelType == std::get<0>(tblgenKey)) && (dimOrdering == std::get<1>(tblgenKey)) && (higherOrdering == std::get<2>(tblgenKey)) && (pointerBitWidth == std::get<3>(tblgenKey)) && (indexBitWidth == std::get<4>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey), std::get<1>(tblgenKey), std::get<2>(tblgenKey), std::get<3>(tblgenKey), std::get<4>(tblgenKey));
  }

  static SparseTensorEncodingAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto dimLevelType = std::get<0>(tblgenKey);
    auto dimOrdering = std::get<1>(tblgenKey);
    auto higherOrdering = std::get<2>(tblgenKey);
    auto pointerBitWidth = std::get<3>(tblgenKey);
    auto indexBitWidth = std::get<4>(tblgenKey);
    dimLevelType = allocator.copyInto(dimLevelType);
    return new (allocator.allocate<SparseTensorEncodingAttrStorage>()) SparseTensorEncodingAttrStorage(dimLevelType, dimOrdering, higherOrdering, pointerBitWidth, indexBitWidth);
  }

  ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType;
  AffineMap dimOrdering;
  AffineMap higherOrdering;
  unsigned pointerBitWidth;
  unsigned indexBitWidth;
};
} // namespace detail
SparseTensorEncodingAttr SparseTensorEncodingAttr::get(::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth) {
  return Base::get(context, dimLevelType, dimOrdering, higherOrdering, pointerBitWidth, indexBitWidth);
}

SparseTensorEncodingAttr SparseTensorEncodingAttr::getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth) {
  return Base::getChecked(emitError, context, dimLevelType, dimOrdering, higherOrdering, pointerBitWidth, indexBitWidth);
}

::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> SparseTensorEncodingAttr::getDimLevelType() const {
  return getImpl()->dimLevelType;
}

AffineMap SparseTensorEncodingAttr::getDimOrdering() const {
  return getImpl()->dimOrdering;
}

AffineMap SparseTensorEncodingAttr::getHigherOrdering() const {
  return getImpl()->higherOrdering;
}

unsigned SparseTensorEncodingAttr::getPointerBitWidth() const {
  return getImpl()->pointerBitWidth;
}

unsigned SparseTensorEncodingAttr::getIndexBitWidth() const {
  return getImpl()->indexBitWidth;
}

} // namespace sparse_tensor
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::sparse_tensor::SparseTensorEncodingAttr)
namespace mlir {
namespace sparse_tensor {
namespace detail {
struct StorageSpecifierKindAttrStorage : public ::mlir::AttributeStorage {
  using KeyTy = std::tuple<::mlir::sparse_tensor::StorageSpecifierKind>;
  StorageSpecifierKindAttrStorage(::mlir::sparse_tensor::StorageSpecifierKind value) : value(value) {}

  KeyTy getAsKey() const {
    return KeyTy(value);
  }

  bool operator==(const KeyTy &tblgenKey) const {
    return (value == std::get<0>(tblgenKey));
  }

  static ::llvm::hash_code hashKey(const KeyTy &tblgenKey) {
    return ::llvm::hash_combine(std::get<0>(tblgenKey));
  }

  static StorageSpecifierKindAttrStorage *construct(::mlir::AttributeStorageAllocator &allocator, const KeyTy &tblgenKey) {
    auto value = std::get<0>(tblgenKey);
    return new (allocator.allocate<StorageSpecifierKindAttrStorage>()) StorageSpecifierKindAttrStorage(value);
  }

  ::mlir::sparse_tensor::StorageSpecifierKind value;
};
} // namespace detail
StorageSpecifierKindAttr StorageSpecifierKindAttr::get(::mlir::MLIRContext *context, ::mlir::sparse_tensor::StorageSpecifierKind value) {
  return Base::get(context, value);
}

::mlir::Attribute StorageSpecifierKindAttr::parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType) {
  ::mlir::Builder odsBuilder(odsParser.getContext());
  ::llvm::SMLoc odsLoc = odsParser.getCurrentLocation();
  (void) odsLoc;
  ::mlir::FailureOr<::mlir::sparse_tensor::StorageSpecifierKind> _result_value;

  // Parse variable 'value'
  _result_value = [&]() -> ::mlir::FailureOr<::mlir::sparse_tensor::StorageSpecifierKind> {
      auto loc = odsParser.getCurrentLocation();
      ::llvm::StringRef enumKeyword;
      if (::mlir::failed(odsParser.parseKeyword(&enumKeyword)))
        return ::mlir::failure();
      auto maybeEnum = ::mlir::sparse_tensor::symbolizeStorageSpecifierKind(enumKeyword);
      if (maybeEnum)
        return *maybeEnum;
      return {(::mlir::LogicalResult)(odsParser.emitError(loc) << "expected " << "::mlir::sparse_tensor::StorageSpecifierKind" << " to be one of: " << "dim_sz" << ", " << "ptr_mem_sz" << ", " << "idx_mem_sz" << ", " << "val_mem_sz")};
    }();
  if (::mlir::failed(_result_value)) {
    odsParser.emitError(odsParser.getCurrentLocation(), "failed to parse SparseTensorStorageSpecifierKindAttr parameter 'value' which is to be a `::mlir::sparse_tensor::StorageSpecifierKind`");
    return {};
  }
  assert(::mlir::succeeded(_result_value));
  return StorageSpecifierKindAttr::get(odsParser.getContext(),
      ::mlir::sparse_tensor::StorageSpecifierKind((*_result_value)));
}

void StorageSpecifierKindAttr::print(::mlir::AsmPrinter &odsPrinter) const {
  ::mlir::Builder odsBuilder(getContext());
  odsPrinter << ' ';
  odsPrinter << stringifyStorageSpecifierKind(getValue());
}

::mlir::sparse_tensor::StorageSpecifierKind StorageSpecifierKindAttr::getValue() const {
  return getImpl()->value;
}

} // namespace sparse_tensor
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::sparse_tensor::StorageSpecifierKindAttr)
namespace mlir {
namespace sparse_tensor {

/// Parse an attribute registered to this dialect.
::mlir::Attribute SparseTensorDialect::parseAttribute(::mlir::DialectAsmParser &parser,
                                      ::mlir::Type type) const {
  ::llvm::SMLoc typeLoc = parser.getCurrentLocation();
  ::llvm::StringRef attrTag;
  {
    ::mlir::Attribute attr;
    auto parseResult = generatedAttributeParser(parser, &attrTag, type, attr);
    if (parseResult.has_value())
      return attr;
  }
  
  parser.emitError(typeLoc) << "unknown attribute `"
      << attrTag << "` in dialect `" << getNamespace() << "`";
  return {};
}
/// Print an attribute registered to this dialect.
void SparseTensorDialect::printAttribute(::mlir::Attribute attr,
                         ::mlir::DialectAsmPrinter &printer) const {
  if (::mlir::succeeded(generatedAttributePrinter(attr, printer)))
    return;
  
}
} // namespace sparse_tensor
} // namespace mlir

#endif  // GET_ATTRDEF_CLASSES

