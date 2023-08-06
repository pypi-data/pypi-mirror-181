/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* AttrDef Declarations                                                       *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_ATTRDEF_CLASSES
#undef GET_ATTRDEF_CLASSES


namespace mlir {
class AsmParser;
class AsmPrinter;
} // namespace mlir
namespace mlir {
namespace sparse_tensor {
class SparseTensorEncodingAttr;
class StorageSpecifierKindAttr;
namespace detail {
struct SparseTensorEncodingAttrStorage;
} // namespace detail
class SparseTensorEncodingAttr : public ::mlir::Attribute::AttrBase<SparseTensorEncodingAttr, ::mlir::Attribute, detail::SparseTensorEncodingAttrStorage, ::mlir::VerifiableTensorEncoding::Trait> {
public:
  using Base::Base;
  /// Returns the type for pointer storage based on pointerBitWidth
  Type getPointerType() const;

  /// Returns the type for index storage based on indexBitWidth
  Type getIndexType() const;
  using Base::getChecked;
public:
  static SparseTensorEncodingAttr get(::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth);
  static SparseTensorEncodingAttr getChecked(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::mlir::MLIRContext *context, ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth);
  static ::mlir::LogicalResult verify(::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError, ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> dimLevelType, AffineMap dimOrdering, AffineMap higherOrdering, unsigned pointerBitWidth, unsigned indexBitWidth);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"encoding"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::llvm::ArrayRef<::mlir::sparse_tensor::DimLevelType> getDimLevelType() const;
  AffineMap getDimOrdering() const;
  AffineMap getHigherOrdering() const;
  unsigned getPointerBitWidth() const;
  unsigned getIndexBitWidth() const;
  ::mlir::LogicalResult verifyEncoding(ArrayRef<int64_t> shape, Type elementType, ::llvm::function_ref<::mlir::InFlightDiagnostic()> emitError) const;
};
namespace detail {
struct StorageSpecifierKindAttrStorage;
} // namespace detail
class StorageSpecifierKindAttr : public ::mlir::Attribute::AttrBase<StorageSpecifierKindAttr, ::mlir::Attribute, detail::StorageSpecifierKindAttrStorage> {
public:
  using Base::Base;
public:
  static StorageSpecifierKindAttr get(::mlir::MLIRContext *context, ::mlir::sparse_tensor::StorageSpecifierKind value);
  static constexpr ::llvm::StringLiteral getMnemonic() {
    return {"kind"};
  }

  static ::mlir::Attribute parse(::mlir::AsmParser &odsParser, ::mlir::Type odsType);
  void print(::mlir::AsmPrinter &odsPrinter) const;
  ::mlir::sparse_tensor::StorageSpecifierKind getValue() const;
};
} // namespace sparse_tensor
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::sparse_tensor::SparseTensorEncodingAttr)
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::sparse_tensor::StorageSpecifierKindAttr)

#endif  // GET_ATTRDEF_CLASSES

