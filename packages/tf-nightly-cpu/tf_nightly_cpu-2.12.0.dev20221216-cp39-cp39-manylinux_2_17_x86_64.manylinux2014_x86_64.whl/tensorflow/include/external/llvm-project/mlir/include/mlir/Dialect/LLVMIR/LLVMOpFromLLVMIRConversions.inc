if (inst->getOpcode() == llvm::Instruction::AShr) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::AShrOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Add) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::AddOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::AddrSpaceCast) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::AddrSpaceCastOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Alloca) {
FailureOr<Value> _llvmir_gen_operand_arraySize = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arraySize))
  return failure();


    auto *allocaInst = cast<llvm::AllocaInst>(inst);
    Type allocatedType = convertType(allocaInst->getAllocatedType());
    unsigned alignment = allocaInst->getAlign().value();
    mapValue(inst) = odsBuilder.create<LLVM::AllocaOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), allocatedType, _llvmir_gen_operand_arraySize.value(), alignment);
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::And) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::AndOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::AtomicCmpXchg) {
FailureOr<Value> _llvmir_gen_operand_ptr = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_ptr))
  return failure();
FailureOr<Value> _llvmir_gen_operand_cmp = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_cmp))
  return failure();
FailureOr<Value> _llvmir_gen_operand_val = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_val))
  return failure();


    auto *cmpXchgInst = cast<llvm::AtomicCmpXchgInst>(inst);
    mapValue(inst) = odsBuilder.create<LLVM::AtomicCmpXchgOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_ptr.value(), _llvmir_gen_operand_cmp.value(), _llvmir_gen_operand_val.value(),
      getLLVMAtomicOrdering(cmpXchgInst->getSuccessOrdering()),
      getLLVMAtomicOrdering(cmpXchgInst->getFailureOrdering()));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::AtomicRMW) {
FailureOr<Value> _llvmir_gen_operand_ptr = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_ptr))
  return failure();
FailureOr<Value> _llvmir_gen_operand_val = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_val))
  return failure();


    auto *atomicInst = cast<llvm::AtomicRMWInst>(inst);
    mapValue(inst) = odsBuilder.create<LLVM::AtomicRMWOp>(translateLoc(inst->getDebugLoc()), convertType(inst->getType()),
        getLLVMAtomicBinOp(atomicInst->getOperation()), _llvmir_gen_operand_ptr.value(), _llvmir_gen_operand_val.value(),
        getLLVMAtomicOrdering(atomicInst->getOrdering()));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::BitCast) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::BitcastOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::ExtractElement) {
FailureOr<Value> _llvmir_gen_operand_vector = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_vector))
  return failure();
FailureOr<Value> _llvmir_gen_operand_position = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_position))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::ExtractElementOp>(
      translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_vector.value(), _llvmir_gen_operand_position.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::ExtractValue) {
FailureOr<Value> _llvmir_gen_operand_container = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_container))
  return failure();


    auto *evInst = cast<llvm::ExtractValueInst>(inst);
    mapValue(inst) = odsBuilder.create<LLVM::ExtractValueOp>(translateLoc(inst->getDebugLoc()),
      _llvmir_gen_operand_container.value(), getPositionFromIndices(evInst->getIndices()));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FAdd) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FAddOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FCmp) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    auto *fCmpInst = cast<llvm::FCmpInst>(inst);
    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FCmpOp>(
      translateLoc(inst->getDebugLoc()), getFCmpPredicate(fCmpInst->getPredicate()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FDiv) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FDivOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FMul) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FMulOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FNeg) {
FailureOr<Value> _llvmir_gen_operand_operand = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_operand))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FNegOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_operand.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FPExt) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FPExtOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FPToSI) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FPToSIOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FPToUI) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FPToUIOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FPTrunc) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FPTruncOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FRem) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FRemOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::FSub) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::FSubOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Fence) {


    llvm::FenceInst *fenceInst = cast<llvm::FenceInst>(inst);
    odsBuilder.create<LLVM::FenceOp>(
      translateLoc(inst->getDebugLoc()),
      getLLVMAtomicOrdering(fenceInst->getOrdering()),
      getLLVMSyncScope(fenceInst));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Freeze) {
FailureOr<Value> _llvmir_gen_operand_val = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_val))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::FreezeOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_val.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::ICmp) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    auto *iCmpInst = cast<llvm::ICmpInst>(inst);
    mapValue(inst) = odsBuilder.create<::mlir::LLVM::ICmpOp>(
      translateLoc(inst->getDebugLoc()), getICmpPredicate(iCmpInst->getPredicate()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::InsertElement) {
FailureOr<Value> _llvmir_gen_operand_vector = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_vector))
  return failure();
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_position = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_position))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::InsertElementOp>(
      translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_vector.value(), _llvmir_gen_operand_value.value(), _llvmir_gen_operand_position.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::InsertValue) {
FailureOr<Value> _llvmir_gen_operand_container = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_container))
  return failure();
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_value))
  return failure();


    auto *ivInst = cast<llvm::InsertValueInst>(inst);
    mapValue(inst) = odsBuilder.create<LLVM::InsertValueOp>(translateLoc(inst->getDebugLoc()),
      _llvmir_gen_operand_container.value(), _llvmir_gen_operand_value.value(), getPositionFromIndices(ivInst->getIndices()));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::IntToPtr) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::IntToPtrOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::LShr) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::LShrOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Load) {
FailureOr<Value> _llvmir_gen_operand_addr = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_addr))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::LoadOp>(translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_addr.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Mul) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::MulOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Or) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::OrOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::PtrToInt) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::PtrToIntOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Resume) {
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_value))
  return failure();


    odsBuilder.create<LLVM::ResumeOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_value.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Ret) {


    FailureOr<SmallVector<Value>> mlirOperands = convertValues(llvmOperands);
    if (failed(mlirOperands))
      return failure();
    odsBuilder.create<LLVM::ReturnOp>(translateLoc(inst->getDebugLoc()), *mlirOperands);
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::SDiv) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::SDivOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::SExt) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::SExtOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::SIToFP) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::SIToFPOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::SRem) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::SRemOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Select) {
FailureOr<Value> _llvmir_gen_operand_condition = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_condition))
  return failure();
FailureOr<Value> _llvmir_gen_operand_trueValue = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_trueValue))
  return failure();
FailureOr<Value> _llvmir_gen_operand_falseValue = convertValue(llvmOperands[2]);
if (failed(_llvmir_gen_operand_falseValue))
  return failure();


    mapValue(inst) = odsBuilder.create<LLVM::SelectOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_condition.value(), _llvmir_gen_operand_trueValue.value(), _llvmir_gen_operand_falseValue.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Shl) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::ShlOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::ShuffleVector) {
FailureOr<Value> _llvmir_gen_operand_v1 = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_v1))
  return failure();
FailureOr<Value> _llvmir_gen_operand_v2 = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_v2))
  return failure();


    auto *svInst = cast<llvm::ShuffleVectorInst>(inst);
    SmallVector<int32_t> mask(svInst->getShuffleMask());
    mapValue(inst) = odsBuilder.create<LLVM::ShuffleVectorOp>(
      translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_v1.value(), _llvmir_gen_operand_v2.value(), mask);
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Store) {
FailureOr<Value> _llvmir_gen_operand_value = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_value))
  return failure();
FailureOr<Value> _llvmir_gen_operand_addr = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_addr))
  return failure();


    odsBuilder.create<LLVM::StoreOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_value.value(), _llvmir_gen_operand_addr.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Sub) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::SubOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Trunc) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::TruncOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::UDiv) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::UDivOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::UIToFP) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::UIToFPOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::URem) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::URemOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Unreachable) {


    odsBuilder.create<LLVM::UnreachableOp>(translateLoc(inst->getDebugLoc()));
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::Xor) {
FailureOr<Value> _llvmir_gen_operand_lhs = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_lhs))
  return failure();
FailureOr<Value> _llvmir_gen_operand_rhs = convertValue(llvmOperands[1]);
if (failed(_llvmir_gen_operand_rhs))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::XOrOp>(translateLoc(inst->getDebugLoc()), _llvmir_gen_operand_lhs.value(), _llvmir_gen_operand_rhs.value());
  
  return success();
}
if (inst->getOpcode() == llvm::Instruction::ZExt) {
FailureOr<Value> _llvmir_gen_operand_arg = convertValue(llvmOperands[0]);
if (failed(_llvmir_gen_operand_arg))
  return failure();


    mapValue(inst) = odsBuilder.create<::mlir::LLVM::ZExtOp>(
      translateLoc(inst->getDebugLoc()), convertType(inst->getType()), _llvmir_gen_operand_arg.value());
  
  return success();
}
