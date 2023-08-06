/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Declarations                                                            *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#if defined(GET_OP_CLASSES) || defined(GET_OP_FWD_DEFINES)
#undef GET_OP_FWD_DEFINES
namespace mlir {
namespace thlo {
class ConcatenateOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class DynamicBroadcastInDimOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class GatherOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class ReverseOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class ScatterOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class SortOp;
} // namespace thlo
} // namespace mlir
namespace mlir {
namespace thlo {
class YieldOp;
} // namespace thlo
} // namespace mlir
#endif

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::ConcatenateOp declarations
//===----------------------------------------------------------------------===//

class ConcatenateOpAdaptor {
public:
  ConcatenateOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ConcatenateOpAdaptor(ConcatenateOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputs();
  ::mlir::Value getInit();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getDimensionAttr();
  ::llvm::APInt getDimension();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ConcatenateOp : public ::mlir::Op<ConcatenateOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::AtLeastNOperands<1>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ConcatenateOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("dimension")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getDimensionAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getDimensionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.concatenate");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputs();
  ::mlir::TypedValue<::mlir::ShapedType> getInit();
  ::mlir::MutableOperandRange getInputsMutable();
  ::mlir::MutableOperandRange getInitMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResult();
  ::mlir::IntegerAttr getDimensionAttr();
  ::llvm::APInt getDimension();
  void setDimensionAttr(::mlir::IntegerAttr attr);
  void setDimension(::llvm::APInt attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::ValueRange inputs, ::mlir::Value init, ::mlir::IntegerAttr dimension);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::ValueRange inputs, ::mlir::Value init, ::llvm::APInt dimension);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - 1, getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::ConcatenateOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::DynamicBroadcastInDimOp declarations
//===----------------------------------------------------------------------===//

class DynamicBroadcastInDimOpAdaptor {
public:
  DynamicBroadcastInDimOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  DynamicBroadcastInDimOpAdaptor(DynamicBroadcastInDimOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOperand();
  ::mlir::Value getInit();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseI64ArrayAttr getBroadcastDimensionsAttr();
  ::llvm::ArrayRef<int64_t> getBroadcastDimensions();
  ::mlir::DenseI64ArrayAttr getKnownExpandingDimensionsAttr();
  ::llvm::Optional<::llvm::ArrayRef<int64_t>> getKnownExpandingDimensions();
  ::mlir::DenseI64ArrayAttr getKnownNonexpandingDimensionsAttr();
  ::llvm::Optional<::llvm::ArrayRef<int64_t>> getKnownNonexpandingDimensions();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class DynamicBroadcastInDimOp : public ::mlir::Op<DynamicBroadcastInDimOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = DynamicBroadcastInDimOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("broadcast_dimensions"), ::llvm::StringRef("known_expanding_dimensions"), ::llvm::StringRef("known_nonexpanding_dimensions")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getBroadcastDimensionsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getBroadcastDimensionsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getKnownExpandingDimensionsAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getKnownExpandingDimensionsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  ::mlir::StringAttr getKnownNonexpandingDimensionsAttrName() {
    return getAttributeNameForIndex(2);
  }

  static ::mlir::StringAttr getKnownNonexpandingDimensionsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 2);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.dynamic_broadcast_in_dim");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getOperand();
  ::mlir::TypedValue<::mlir::ShapedType> getInit();
  ::mlir::MutableOperandRange getOperandMutable();
  ::mlir::MutableOperandRange getInitMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResult();
  ::mlir::DenseI64ArrayAttr getBroadcastDimensionsAttr();
  ::llvm::ArrayRef<int64_t> getBroadcastDimensions();
  ::mlir::DenseI64ArrayAttr getKnownExpandingDimensionsAttr();
  ::llvm::Optional<::llvm::ArrayRef<int64_t>> getKnownExpandingDimensions();
  ::mlir::DenseI64ArrayAttr getKnownNonexpandingDimensionsAttr();
  ::llvm::Optional<::llvm::ArrayRef<int64_t>> getKnownNonexpandingDimensions();
  void setBroadcastDimensionsAttr(::mlir::DenseI64ArrayAttr attr);
  void setBroadcastDimensions(::llvm::ArrayRef<int64_t> attrValue);
  void setKnownExpandingDimensionsAttr(::mlir::DenseI64ArrayAttr attr);
  void setKnownExpandingDimensions(::llvm::Optional<::llvm::ArrayRef<int64_t>> attrValue);
  void setKnownNonexpandingDimensionsAttr(::mlir::DenseI64ArrayAttr attr);
  void setKnownNonexpandingDimensions(::llvm::Optional<::llvm::ArrayRef<int64_t>> attrValue);
  ::mlir::Attribute removeKnownExpandingDimensionsAttr();
  ::mlir::Attribute removeKnownNonexpandingDimensionsAttr();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::Value operand, ::mlir::Value init, ::mlir::DenseI64ArrayAttr broadcast_dimensions, /*optional*/::mlir::DenseI64ArrayAttr known_expanding_dimensions, /*optional*/::mlir::DenseI64ArrayAttr known_nonexpanding_dimensions);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::Value operand, ::mlir::Value init, ::llvm::ArrayRef<int64_t> broadcast_dimensions, /*optional*/::mlir::DenseI64ArrayAttr known_expanding_dimensions, /*optional*/::mlir::DenseI64ArrayAttr known_nonexpanding_dimensions);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 3 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - 1, getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::DynamicBroadcastInDimOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::GatherOp declarations
//===----------------------------------------------------------------------===//

class GatherOpAdaptor {
public:
  GatherOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  GatherOpAdaptor(GatherOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getOperand();
  ::mlir::Value getStartIndices();
  ::mlir::Value getInit();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class GatherOp : public ::mlir::Op<GatherOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<3>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = GatherOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.gather");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getOperand();
  ::mlir::TypedValue<::mlir::ShapedType> getStartIndices();
  ::mlir::TypedValue<::mlir::ShapedType> getInit();
  ::mlir::MutableOperandRange getOperandMutable();
  ::mlir::MutableOperandRange getStartIndicesMutable();
  ::mlir::MutableOperandRange getInitMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResult();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::Value operand, ::mlir::Value start_indices, ::mlir::Value init);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
public:

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - 1, getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::GatherOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::ReverseOp declarations
//===----------------------------------------------------------------------===//

class ReverseOpAdaptor {
public:
  ReverseOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ReverseOpAdaptor(ReverseOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getInput();
  ::mlir::Value getInit();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::DenseI64ArrayAttr getReverseDimensionsAttr();
  ::llvm::ArrayRef<int64_t> getReverseDimensions();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ReverseOp : public ::mlir::Op<ReverseOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::OneResult, ::mlir::OpTrait::OneTypedResult<::mlir::ShapedType>::Impl, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<2>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait, ::mlir::OpAsmOpInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ReverseOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("reverse_dimensions")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getReverseDimensionsAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getReverseDimensionsAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.reverse");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getInput();
  ::mlir::TypedValue<::mlir::ShapedType> getInit();
  ::mlir::MutableOperandRange getInputMutable();
  ::mlir::MutableOperandRange getInitMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getResult();
  ::mlir::DenseI64ArrayAttr getReverseDimensionsAttr();
  ::llvm::ArrayRef<int64_t> getReverseDimensions();
  void setReverseDimensionsAttr(::mlir::DenseI64ArrayAttr attr);
  void setReverseDimensions(::llvm::ArrayRef<int64_t> attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value input, ::mlir::Value init, ::mlir::DenseI64ArrayAttr reverse_dimensions);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value input, ::mlir::Value init, ::mlir::DenseI64ArrayAttr reverse_dimensions);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Type result, ::mlir::Value input, ::mlir::Value init, ::llvm::ArrayRef<int64_t> reverse_dimensions);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value input, ::mlir::Value init, ::llvm::ArrayRef<int64_t> reverse_dimensions);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
  void getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 1 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - 1, getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::ReverseOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::ScatterOp declarations
//===----------------------------------------------------------------------===//

class ScatterOpAdaptor {
public:
  ScatterOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  ScatterOpAdaptor(ScatterOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::Value getIndices();
  ::mlir::Value getUpdates();
  ::mlir::Value getInit();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::Region &getUpdateComputation();
  ::mlir::RegionRange getRegions();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class ScatterOp : public ::mlir::Op<ScatterOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::NOperands<3>::Impl, ::mlir::OpTrait::SingleBlockImplicitTerminator<YieldOp>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = ScatterOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.scatter");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::TypedValue<::mlir::ShapedType> getIndices();
  ::mlir::TypedValue<::mlir::ShapedType> getUpdates();
  ::mlir::TypedValue<::mlir::ShapedType> getInit();
  ::mlir::MutableOperandRange getIndicesMutable();
  ::mlir::MutableOperandRange getUpdatesMutable();
  ::mlir::MutableOperandRange getInitMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResult();
  ::mlir::Region &getUpdateComputation();
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::Value indices, ::mlir::Value updates, ::mlir::Value init);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
public:

      // Returns index vector dimension size, which is always statically-known.
      int64_t getIndexVectorDimSize() {
        return getIndices().getType().getDimSize(1);
      }

      // Returns the number of indices, i.e. number of scalar/tensor updates.
      int64_t getIndicesCount() { return getIndices().getType().getDimSize(0); }

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - 1, getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::ScatterOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::SortOp declarations
//===----------------------------------------------------------------------===//

class SortOpAdaptor {
public:
  SortOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  SortOpAdaptor(SortOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getInputs();
  ::mlir::ValueRange getInits();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::IntegerAttr getDimensionAttr();
  ::llvm::APInt getDimension();
  ::mlir::BoolAttr getIsStableAttr();
  bool getIsStable();
  ::mlir::Region &getComparator();
  ::mlir::RegionRange getRegions();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class SortOp : public ::mlir::Op<SortOp, ::mlir::OpTrait::OneRegion, ::mlir::OpTrait::VariadicResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::SingleBlockImplicitTerminator<YieldOp>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::DestinationStyleOpInterface::Trait, ::mlir::OpAsmOpInterface::Trait, ::mlir::gml_st::TilingInterface::Trait> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = SortOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    static ::llvm::StringRef attrNames[] = {::llvm::StringRef("dimension"), ::llvm::StringRef("is_stable")};
    return ::llvm::makeArrayRef(attrNames);
  }

  ::mlir::StringAttr getDimensionAttrName() {
    return getAttributeNameForIndex(0);
  }

  static ::mlir::StringAttr getDimensionAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 0);
  }

  ::mlir::StringAttr getIsStableAttrName() {
    return getAttributeNameForIndex(1);
  }

  static ::mlir::StringAttr getIsStableAttrName(::mlir::OperationName name) {
    return getAttributeNameForIndex(name, 1);
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.sort");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getInputs();
  ::mlir::Operation::operand_range getInits();
  ::mlir::MutableOperandRange getInputsMutable();
  ::mlir::MutableOperandRange getInitsMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  ::mlir::Operation::result_range getResult();
  ::mlir::Region &getComparator();
  ::mlir::IntegerAttr getDimensionAttr();
  ::llvm::APInt getDimension();
  ::mlir::BoolAttr getIsStableAttr();
  bool getIsStable();
  void setDimensionAttr(::mlir::IntegerAttr attr);
  void setDimension(::llvm::APInt attrValue);
  void setIsStableAttr(::mlir::BoolAttr attr);
  void setIsStable(bool attrValue);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::ValueRange inputs, ::mlir::ValueRange inits, ::mlir::IntegerAttr dimension, ::mlir::BoolAttr is_stable);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange result, ::mlir::ValueRange inputs, ::mlir::ValueRange inits, ::llvm::APInt dimension, bool is_stable);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &p);
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  void getAsmResultNames(::mlir::OpAsmSetValueNameFn setNameFn);
  void getAsmBlockArgumentNames(::mlir::Region&region, ::mlir::OpAsmSetValueNameFn setNameFn);
  SmallVector<utils::IteratorType> getLoopIteratorTypes();
  SmallVector<Range> getIterationDomain(OpBuilder &b);
  SmallVector<Operation*> getTiledImplementation(OpBuilder &b, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes, bool useExtractSlice);
  LogicalResult getResultTilePosition(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult>  offsets, ArrayRef<OpFoldResult>  sizes, SmallVector<OpFoldResult> &resultOffsets, SmallVector<OpFoldResult> &resultSizes);
  FailureOr<Value> generateResultTileValue(OpBuilder &b, unsigned resultNumber, ArrayRef<OpFoldResult> offsets, ArrayRef<OpFoldResult> sizes);
private:
  ::mlir::StringAttr getAttributeNameForIndex(unsigned index) {
    return getAttributeNameForIndex((*this)->getName(), index);
  }

  static ::mlir::StringAttr getAttributeNameForIndex(::mlir::OperationName name, unsigned index) {
    assert(index < 2 && "invalid attribute index");
    assert(name.getStringRef() == getOperationName() && "invalid operation name");
    return name.getRegisteredInfo()->getAttributeNames()[index];
  }

public:

      // Implement method necessary for DestinationStyleOpInterface.
      std::pair<int64_t, int64_t> getDpsInitsPositionRange() {
        int64_t getNumOperands = this->getNumOperands();
        return {getNumOperands - getInits().size(), getNumOperands};
      }
    };
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::SortOp)

namespace mlir {
namespace thlo {

//===----------------------------------------------------------------------===//
// ::mlir::thlo::YieldOp declarations
//===----------------------------------------------------------------------===//

class YieldOpAdaptor {
public:
  YieldOpAdaptor(::mlir::ValueRange values, ::mlir::DictionaryAttr attrs = nullptr, ::mlir::RegionRange regions = {});

  YieldOpAdaptor(YieldOp op);

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::ValueRange getODSOperands(unsigned index);
  ::mlir::ValueRange getValues();
  ::mlir::ValueRange getOperands();
  ::mlir::DictionaryAttr getAttributes();
  ::mlir::LogicalResult verify(::mlir::Location loc);
private:
  ::mlir::ValueRange odsOperands;
  ::mlir::DictionaryAttr odsAttrs;
  ::mlir::RegionRange odsRegions;
  ::llvm::Optional<::mlir::OperationName> odsOpName;
};
class YieldOp : public ::mlir::Op<YieldOp, ::mlir::OpTrait::ZeroRegions, ::mlir::OpTrait::ZeroResults, ::mlir::OpTrait::ZeroSuccessors, ::mlir::OpTrait::VariadicOperands, ::mlir::OpTrait::HasParent<ScatterOp, SortOp>::Impl, ::mlir::OpTrait::OpInvariants, ::mlir::ConditionallySpeculatable::Trait, ::mlir::OpTrait::AlwaysSpeculatableImplTrait, ::mlir::MemoryEffectOpInterface::Trait, ::mlir::OpTrait::ReturnLike, ::mlir::OpTrait::IsTerminator> {
public:
  using Op::Op;
  using Op::print;
  using Adaptor = YieldOpAdaptor;
public:
  static ::llvm::ArrayRef<::llvm::StringRef> getAttributeNames() {
    return {};
  }

  static constexpr ::llvm::StringLiteral getOperationName() {
    return ::llvm::StringLiteral("thlo.yield");
  }

  std::pair<unsigned, unsigned> getODSOperandIndexAndLength(unsigned index);
  ::mlir::Operation::operand_range getODSOperands(unsigned index);
  ::mlir::Operation::operand_range getValues();
  ::mlir::MutableOperandRange getValuesMutable();
  std::pair<unsigned, unsigned> getODSResultIndexAndLength(unsigned index);
  ::mlir::Operation::result_range getODSResults(unsigned index);
  static void build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::ValueRange values);
  static void build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes = {});
  ::mlir::LogicalResult verifyInvariantsImpl();
  ::mlir::LogicalResult verifyInvariants();
  ::mlir::LogicalResult verify();
  static ::mlir::ParseResult parse(::mlir::OpAsmParser &parser, ::mlir::OperationState &result);
  void print(::mlir::OpAsmPrinter &_odsPrinter);
  void getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects);
public:
};
} // namespace thlo
} // namespace mlir
MLIR_DECLARE_EXPLICIT_TYPE_ID(::mlir::thlo::YieldOp)


#endif  // GET_OP_CLASSES

