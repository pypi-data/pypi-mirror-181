if (intrinsicID == llvm::Intrinsic::abs) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::AbsOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::assume) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::AssumeOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::bitreverse) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::BitReverseOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::copysign) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CopySignOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_align) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroAlignOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_begin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroBeginOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_end) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroEndOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_free) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroFreeOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_id) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroIdOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_resume) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroResumeOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_save) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroSaveOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_size) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroSizeOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::coro_suspend) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CoroSuspendOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::cos) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CosOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::ctlz) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CountLeadingZerosOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::cttz) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CountTrailingZerosOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::ctpop) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::CtPopOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::dbg_addr) {
FailureOr<Value> _llvmir_gen_operand_addr = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_addr))
  return failure();


    // Drop all debug intrinsics with a non-empty debug expression.
    // TODO: Stop dropping debug intrinsics once debug expressions are
    // convertible to MLIR.
    auto *dbgIntr = cast<llvm::DbgVariableIntrinsic>(inst);
    if (dbgIntr->getExpression()->getNumElements() == 0)
      odsBuilder.create<::mlir::LLVM::DbgAddrOp>(translateLoc(inst->getDebugLoc()),
        _llvmir_gen_operand_addr.value(), matchLocalVariableAttr(llvmOperands[1]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::dbg_declare) {
FailureOr<Value> _llvmir_gen_operand_addr = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_addr))
  return failure();


    // Drop all debug intrinsics with a non-empty debug expression.
    // TODO: Stop dropping debug intrinsics once debug expressions are
    // convertible to MLIR.
    auto *dbgIntr = cast<llvm::DbgVariableIntrinsic>(inst);
    if (dbgIntr->getExpression()->getNumElements() == 0)
      odsBuilder.create<::mlir::LLVM::DbgDeclareOp>(translateLoc(inst->getDebugLoc()),
        _llvmir_gen_operand_addr.value(), matchLocalVariableAttr(llvmOperands[1]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::dbg_value) {
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_value))
  return failure();


    // Drop all debug intrinsics with a non-empty debug expression.
    // TODO: Stop dropping debug intrinsics once debug expressions are
    // convertible to MLIR.
    auto *dbgIntr = cast<llvm::DbgVariableIntrinsic>(inst);
    if (dbgIntr->getExpression()->getNumElements() == 0)
      odsBuilder.create<::mlir::LLVM::DbgValueOp>(translateLoc(inst->getDebugLoc()),
        _llvmir_gen_operand_value.value(), matchLocalVariableAttr(llvmOperands[1]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::eh_typeid_for) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::EhTypeidForOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::exp2) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::Exp2Op>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::exp) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::ExpOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::fabs) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FAbsOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::ceil) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FCeilOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::floor) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FFloorOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::fma) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FMAOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::fmuladd) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FMulAddOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::trunc) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::FTruncOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::get_active_lane_mask) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::GetActiveLaneMaskOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::is_fpclass) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::IsFPClass>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::lifetime_end) {
FailureOr<Value> _llvmir_gen_operand_ptr = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_ptr))
  return failure();


    odsBuilder.create<LLVM::LifetimeEndOp>(
      translateLoc(inst->getDebugLoc()), matchIntegerAttr(llvmOperands[0]), _llvmir_gen_operand_ptr.value());
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::lifetime_start) {
FailureOr<Value> _llvmir_gen_operand_ptr = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_ptr))
  return failure();


    odsBuilder.create<LLVM::LifetimeStartOp>(
      translateLoc(inst->getDebugLoc()), matchIntegerAttr(llvmOperands[0]), _llvmir_gen_operand_ptr.value());
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::log10) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::Log10Op>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::log2) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::Log2Op>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::log) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::LogOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_load) {
FailureOr<Value> _llvmir_gen_operand_data = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_data))
  return failure();
FailureOr<Value> _llvmir_gen_operand_mask = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_mask))
  return failure();
FailureOr<SmallVector<Value>> _llvmir_gen_operand_pass_thru = convertValues(llvmOperands.drop_front(3));
if (failed(_llvmir_gen_operand_pass_thru))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::MaskedLoadOp>(translateLoc(inst->getDebugLoc()),
      convertType(inst->getType()), _llvmir_gen_operand_data.value(), _llvmir_gen_operand_mask.value(), _llvmir_gen_operand_pass_thru.value(), matchIntegerAttr(llvmOperands[1]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_store) {
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_data = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_data))
  return failure();
FailureOr<Value> _llvmir_gen_operand_mask = convertValue(llvmOperands[3]);
if (failed(_llvmir_gen_operand_mask))
  return failure();


    odsBuilder.create<LLVM::MaskedStoreOp>(translateLoc(inst->getDebugLoc()),
      _llvmir_gen_operand_value.value(), _llvmir_gen_operand_data.value(), _llvmir_gen_operand_mask.value(), matchIntegerAttr(llvmOperands[2]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::matrix_column_major_load) {
FailureOr<Value> _llvmir_gen_operand_data = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_data))
  return failure();
FailureOr<Value> _llvmir_gen_operand_stride = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_stride))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::MatrixColumnMajorLoadOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_data.value(), _llvmir_gen_operand_stride.value(),
      matchIntegerAttr(llvmOperands[2]), matchIntegerAttr(llvmOperands[3]), matchIntegerAttr(llvmOperands[4]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::matrix_column_major_store) {
FailureOr<Value> _llvmir_gen_operand_matrix = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_matrix))
  return failure();
FailureOr<Value> _llvmir_gen_operand_data = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_data))
  return failure();
FailureOr<Value> _llvmir_gen_operand_stride = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_stride))
  return failure();


    odsBuilder.create<LLVM::MatrixColumnMajorStoreOp>(
      translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_matrix.value(), _llvmir_gen_operand_data.value(), _llvmir_gen_operand_stride.value(),
      matchIntegerAttr(llvmOperands[3]), matchIntegerAttr(llvmOperands[4]), matchIntegerAttr(llvmOperands[5]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::matrix_multiply) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::MatrixMultiplyOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value(),
      matchIntegerAttr(llvmOperands[2]), matchIntegerAttr(llvmOperands[3]), matchIntegerAttr(llvmOperands[4]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::matrix_transpose) {
FailureOr<Value> _llvmir_gen_operand_matrix = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_matrix))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::MatrixTransposeOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_matrix.value(),
      matchIntegerAttr(llvmOperands[1]), matchIntegerAttr(llvmOperands[2]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::maxnum) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::MaxNumOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::maximum) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::MaximumOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::memcpy_inline) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::MemcpyInlineOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::memcpy) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::MemcpyOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::memmove) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::MemmoveOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::memset) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::MemsetOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::minnum) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::MinNumOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::minimum) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::MinimumOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::powi) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::PowIOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::pow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::PowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::prefetch) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::Prefetch>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::roundeven) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::RoundEvenOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::round) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::RoundOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::sadd_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SAddWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::smax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SMaxOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::smin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::smul_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SMulWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::ssub_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SSubWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::sin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::sqrt) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::SqrtOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::stackrestore) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::StackRestoreOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::stacksave) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::StackSaveOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::experimental_stepvector) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::StepVectorOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::uadd_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::UAddWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::umax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::UMaxOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::umin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::UMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::umul_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::UMulWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::usub_with_overflow) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::USubWithOverflowOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_ashr) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPAShrOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_add) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPAddOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_and) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPAndOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fadd) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFAddOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fdiv) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFDivOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fmul) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFMulOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fneg) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFNegOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fpext) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFPExtOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fptosi) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFPToSIOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fptoui) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFPToUIOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fptrunc) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFPTruncOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_frem) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFRemOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fsub) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFSubOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_fma) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPFmaOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_inttoptr) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPIntToPtrOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_lshr) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPLShrOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_load) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPLoadOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_merge) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPMergeMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_mul) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPMulOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_or) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPOrOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_ptrtoint) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPPtrToIntOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_add) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceAddOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_and) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceAndOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_fadd) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceFAddOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_fmax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceFMaxOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_fmin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceFMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_fmul) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceFMulOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_mul) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceMulOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_or) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceOrOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_smax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceSMaxOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_smin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceSMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_umax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceUMaxOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_umin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceUMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_reduce_xor) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPReduceXorOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_sdiv) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSDivOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_sext) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSExtOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_sitofp) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSIToFPOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_srem) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSRemOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_select) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSelectMinOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_shl) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPShlOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_store) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPStoreOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::experimental_vp_strided_load) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPStridedLoadOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::experimental_vp_strided_store) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPStridedStoreOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_sub) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPSubOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_trunc) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPTruncOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_udiv) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPUDivOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_uitofp) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPUIToFPOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_urem) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPURemOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_xor) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPXorOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vp_zext) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::VPZExtOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vacopy) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::VaCopyOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::vaend) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::VaEndOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::vastart) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::VaStartOp>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_compressstore) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {};
    Operation *op = odsBuilder.create<::mlir::LLVM::masked_compressstore>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    (void)op;
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_expandload) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::masked_expandload>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_gather) {
FailureOr<Value> _llvmir_gen_operand_ptrs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_ptrs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_mask = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_mask))
  return failure();
FailureOr<SmallVector<Value>> _llvmir_gen_operand_pass_thru = convertValues(llvmOperands.drop_front(3));
if (failed(_llvmir_gen_operand_pass_thru))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::masked_gather>(translateLoc(inst->getDebugLoc()),
      convertType(inst->getType()), _llvmir_gen_operand_ptrs.value(), _llvmir_gen_operand_mask.value(), _llvmir_gen_operand_pass_thru.value(), matchIntegerAttr(llvmOperands[1]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::masked_scatter) {
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_ptrs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_ptrs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_mask = convertValue(llvmOperands[3]);
if (failed(_llvmir_gen_operand_mask))
  return failure();


    odsBuilder.create<LLVM::masked_scatter>(translateLoc(inst->getDebugLoc()),
      _llvmir_gen_operand_value.value(), _llvmir_gen_operand_ptrs.value(), _llvmir_gen_operand_mask.value(), matchIntegerAttr(llvmOperands[2]));
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_add) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_add>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_and) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_and>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_fadd) {
FailureOr<Value> _llvmir_gen_operand_start_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_start_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_input = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_input))
  return failure();


    bool allowReassoc = inst->getFastMathFlags().allowReassoc();
    mapValue(inst) = odsBuilder.create<::mlir::LLVM::vector_reduce_fadd>(translateLoc(inst->getDebugLoc()),
      convertType(inst->getType()), _llvmir_gen_operand_start_value.value(), _llvmir_gen_operand_input.value(), allowReassoc);
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_fmax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_fmax>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_fmin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_fmin>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_fmul) {
FailureOr<Value> _llvmir_gen_operand_start_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_start_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_input = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_input))
  return failure();


    bool allowReassoc = inst->getFastMathFlags().allowReassoc();
    mapValue(inst) = odsBuilder.create<::mlir::LLVM::vector_reduce_fmul>(translateLoc(inst->getDebugLoc()),
      convertType(inst->getType()), _llvmir_gen_operand_start_value.value(), _llvmir_gen_operand_input.value(), allowReassoc);
  
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_mul) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_mul>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_or) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_or>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_smax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_smax>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_smin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_smin>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_umax) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_umax>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_umin) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_umin>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vector_reduce_xor) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vector_reduce_xor>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
if (intrinsicID == llvm::Intrinsic::vscale) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    SmallVector<Type> resultTypes =
    {convertType(inst->getType())};
    Operation *op = odsBuilder.create<::mlir::LLVM::vscale>(
      translateLoc(inst->getDebugLoc()), resultTypes, *mlirOperands);
    mapValue(inst) = op->getResult(0);
  return success();
}
