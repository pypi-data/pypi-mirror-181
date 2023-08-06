from typing import List, Optional
from .asts import AST, _interface

_property = property


class TerminalSymbol(AST):
    pass


class NormalScopeAST(AST):
    @_property
    def system_headers(self) -> List[AST]:
        return self.child_slot("system_headers")  # type: ignore

    @_property
    def project_directory(self) -> Optional[AST]:
        return self.child_slot("project_directory")  # type: ignore


class CLikeSyntaxAST(AST):
    pass


class CXXAST(AST):
    pass


class CAST(CXXAST, CLikeSyntaxAST, NormalScopeAST, AST):
    pass


class CNewline(CAST, TerminalSymbol, AST):
    pass


class CXXLogicalNot(AST):
    pass


class CLogicalNot(CXXLogicalNot, CAST, TerminalSymbol, AST):
    pass


class CXXNotEqual(AST):
    pass


class CNotEqual(CXXNotEqual, CAST, TerminalSymbol, AST):
    pass


class CDoubleQuote(CAST, TerminalSymbol, AST):
    pass


class CXXMacroDefine(AST):
    pass


class CMacroDefine(CXXMacroDefine, CAST, AST):
    pass


class CXXMacroElif(AST):
    pass


class CMacroElif(CXXMacroElif, CAST, AST):
    pass


class CXXMacroElse(AST):
    pass


class CMacroElse(CXXMacroElse, CAST, AST):
    pass


class CXXMacroEndIf(AST):
    pass


class CMacroEndIf(CXXMacroEndIf, CAST, AST):
    pass


class CXXMacroIf(AST):
    pass


class CMacroIf(CXXMacroIf, CAST, AST):
    pass


class CXXMacroIfDefined(AST):
    pass


class CMacroIfDefined(CXXMacroIfDefined, CAST, AST):
    pass


class CXXMacroIfNotDefined(AST):
    pass


class CMacroIfNotDefined(CXXMacroIfNotDefined, CAST, AST):
    pass


class CXXMacroInclude(AST):
    pass


class CMacroInclude(CXXMacroInclude, CAST, AST):
    pass


class CXXModulo(AST):
    pass


class CModulo(CXXModulo, CAST, TerminalSymbol, AST):
    pass


class CModuleAssign(CAST, TerminalSymbol, AST):
    pass


class CXXBitwiseAnd(AST):
    pass


class CBitwiseAnd(CXXBitwiseAnd, CAST, TerminalSymbol, AST):
    pass


class CXXLogicalAnd(AST):
    pass


class CLogicalAnd(CXXLogicalAnd, CAST, TerminalSymbol, AST):
    pass


class CBitwiseAndAssign(CAST, TerminalSymbol, AST):
    pass


class CSingleQuote(CAST, TerminalSymbol, AST):
    pass


class COpenParenthesis(CAST, TerminalSymbol, AST):
    pass


class CCloseParenthesis(CAST, TerminalSymbol, AST):
    pass


class CXXMultiply(AST):
    pass


class CMultiply(CXXMultiply, CAST, TerminalSymbol, AST):
    pass


class CMultiplyAssign(CAST, TerminalSymbol, AST):
    pass


class CXXAdd(AST):
    pass


class CAdd(CXXAdd, CAST, TerminalSymbol, AST):
    pass


class CXXIncrement(AST):
    pass


class CIncrement(CXXIncrement, CAST, TerminalSymbol, AST):
    pass


class CAddAssign(CAST, TerminalSymbol, AST):
    pass


class CComma(CAST, TerminalSymbol, AST):
    pass


class CXXSubtract(AST):
    pass


class CSubtract(CXXSubtract, CAST, TerminalSymbol, AST):
    pass


class CXXDecrement(AST):
    pass


class CDecrement(CXXDecrement, CAST, TerminalSymbol, AST):
    pass


class CAttributeSubtract(CAST, TerminalSymbol, AST):
    pass


class CBased(CAST, TerminalSymbol, AST):
    pass


class CCdecl(CAST, TerminalSymbol, AST):
    pass


class CClrcall(CAST, TerminalSymbol, AST):
    pass


class CDeclspec(CAST, TerminalSymbol, AST):
    pass


class CFastcall(CAST, TerminalSymbol, AST):
    pass


class CStdcall(CAST, TerminalSymbol, AST):
    pass


class CThiscall(CAST, TerminalSymbol, AST):
    pass


class CUnderscoreUnaligned(CAST, TerminalSymbol, AST):
    pass


class CVectorcall(CAST, TerminalSymbol, AST):
    pass


class CSubtractAssign(CAST, TerminalSymbol, AST):
    pass


class CXXDashArrow(AST):
    pass


class CDashArrow(CXXDashArrow, CAST, TerminalSymbol, AST):
    pass


class CAbstractDeclarator(CAST, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CAtomic(CAST, TerminalSymbol, AST):
    pass


class CXXDeclarator(AST):
    pass


class CDeclarator(CXXDeclarator, CAST, AST):
    pass


class ExpressionAST(AST):
    pass


class CXXExpression(ExpressionAST, AST):
    pass


class CExpression(CXXExpression, CAST, AST):
    pass


class CFieldDeclarator(CAST, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class StatementAST(AST):
    pass


class CXXStatement(StatementAST, AST):
    pass


class CStatement(CXXStatement, CAST, AST):
    pass


class CTypeDeclarator(CAST, AST):
    pass


class CTypeSpecifier(CAST, AST):
    pass


class CUnaligned(CAST, TerminalSymbol, AST):
    pass


class CDot(CAST, TerminalSymbol, AST):
    pass


class CEllipsis(CAST, TerminalSymbol, AST):
    pass


class CXXDivide(AST):
    pass


class CDivide(CXXDivide, CAST, TerminalSymbol, AST):
    pass


class CDivideAssign(CAST, TerminalSymbol, AST):
    pass


class CColon(CAST, TerminalSymbol, AST):
    pass


class CScopeResolution(CAST, TerminalSymbol, AST):
    pass


class CSemicolon(CAST, TerminalSymbol, AST):
    pass


class CXXLessThan(AST):
    pass


class CLessThan(CXXLessThan, CAST, TerminalSymbol, AST):
    pass


class CXXBitshiftLeft(AST):
    pass


class CBitshiftLeft(CXXBitshiftLeft, CAST, TerminalSymbol, AST):
    pass


class CBitshiftLeftAssign(CAST, TerminalSymbol, AST):
    pass


class CXXLessThanOrEqual(AST):
    pass


class CLessThanOrEqual(CXXLessThanOrEqual, CAST, TerminalSymbol, AST):
    pass


class CAssign(CAST, TerminalSymbol, AST):
    pass


class CXXEqual(AST):
    pass


class CEqual(CXXEqual, CAST, TerminalSymbol, AST):
    pass


class CXXGreaterThan(AST):
    pass


class CGreaterThan(CXXGreaterThan, CAST, TerminalSymbol, AST):
    pass


class CXXGreaterThanOrEqual(AST):
    pass


class CGreaterThanOrEqual(CXXGreaterThanOrEqual, CAST, TerminalSymbol, AST):
    pass


class CXXBitshiftRight(AST):
    pass


class CBitshiftRight(CXXBitshiftRight, CAST, TerminalSymbol, AST):
    pass


class CBitshiftRightAssign(CAST, TerminalSymbol, AST):
    pass


class CQuestion(CAST, TerminalSymbol, AST):
    pass


class CXXAbstractArrayDeclarator(AST):
    @_property
    def size_child_slot(self) -> Optional[AST]:
        return self.child_slot("size_child_slot")  # type: ignore


class CAbstractArrayDeclarator(CAbstractDeclarator, CXXAbstractArrayDeclarator, AST):
    pass


class CXXAbstractFunctionDeclarator(AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class CAbstractFunctionDeclarator(CAbstractDeclarator, CXXAbstractFunctionDeclarator, AST):
    pass


class CAbstractParenthesizedDeclarator(CAbstractDeclarator, AST):
    pass


class CXXAbstractPointerDeclarator(AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CAbstractPointerDeclarator(CAbstractDeclarator, CXXAbstractPointerDeclarator, AST):
    pass


class ArgumentsAST(AST):
    pass


class CXXArgumentList(ArgumentsAST, AST):
    pass


class CArgumentList(CXXArgumentList, CAST, AST):
    pass


class CArgumentList0(CArgumentList, AST):
    pass


class CArgumentList1(CArgumentList, AST):
    pass


class CXXArrayDeclarator(AST):
    @_property
    def size_child_slot(self) -> Optional[AST]:
        return self.child_slot("size_child_slot")  # type: ignore


class CArrayDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXArrayDeclarator, AST):
    pass


class AssignmentAST(AST):
    pass


class CXXAssignmentExpression(AssignmentAST, AST):
    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore


class CAssignmentExpression(CExpression, CXXAssignmentExpression, AST):
    pass


class CAttribute(CAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def prefix(self) -> Optional[AST]:
        return self.child_slot("prefix")  # type: ignore


class CAttribute0(CAttribute, AST):
    pass


class CAttribute1(CAttribute, AST):
    pass


class CAttribute2(CAttribute, AST):
    pass


class CAttribute3(CAttribute, AST):
    pass


class CAttributeDeclaration(CAST, AST):
    pass


class CAttributeSpecifier(CAST, AST):
    pass


class CAttributedDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, AST):
    pass


class CAttributedStatement(CAST, AST):
    pass


class CAttributedStatement0(CAttributedStatement, AST):
    pass


class CAttributedStatement1(CAttributedStatement, AST):
    pass


class CAuto(CAST, TerminalSymbol, AST):
    pass


class BinaryAST(ExpressionAST, AST):
    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore


class CXXBinaryExpression(BinaryAST, AST):
    pass


class CBinaryExpression(CExpression, CXXBinaryExpression, AST):
    pass


class CBinaryExpression0(CBinaryExpression, AST):
    pass


class CBinaryExpression1(CBinaryExpression, AST):
    pass


class CBitfieldClause(CAST, AST):
    pass


class TextFragment(AST):
    pass


class Blot(TextFragment, AST):
    pass


class CBlot(CAST, Blot, AST):
    pass


class CBreak(CAST, TerminalSymbol, AST):
    pass


class CXXBreakStatement(AST):
    pass


class CBreakStatement(CStatement, CXXBreakStatement, AST):
    pass


class CallAST(ExpressionAST, AST):
    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore

    @_property
    def function(self) -> Optional[AST]:
        return self.child_slot("function")  # type: ignore

    def call_function(self: "CallAST") -> AST:
        """Return the call function of this AST."""
        return _interface.dispatch(CallAST.call_function.__name__, self)

    def call_arguments(self: "CallAST") -> List[AST]:
        """Return the call arguments of this AST."""
        return _interface.dispatch(CallAST.call_arguments.__name__, self) or []


class CXXCallExpression(CallAST, AST):
    pass


class CCallExpression(CExpression, CXXCallExpression, AST):
    pass


class CCase(CAST, TerminalSymbol, AST):
    pass


class ControlFlowAST(AST):
    pass


class CXXCaseStatement(ControlFlowAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def statements(self) -> List[AST]:
        return self.child_slot("statements")  # type: ignore


class CCaseStatement(CStatement, CXXCaseStatement, AST):
    pass


class CCaseStatement0(CCaseStatement, AST):
    pass


class CCaseStatement1(CCaseStatement, AST):
    pass


class CXXCastExpression(AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CCastExpression(CExpression, CXXCastExpression, AST):
    pass


class LiteralAST(AST):
    pass


class CharAST(LiteralAST, AST):
    pass


class CXXCharLiteral(CharAST, AST):
    pass


class CCharLiteral(CExpression, CXXCharLiteral, AST):
    pass


class CXXCommaExpression(ExpressionAST, AST):
    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore


class CCommaExpression(CXXCommaExpression, CAST, AST):
    pass


class CommentAST(AST):
    pass


class CXXComment(CommentAST, AST):
    pass


class CComment(CXXComment, CAST, AST):
    pass


class CCompoundLiteralExpression(CExpression, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class CompoundAST(AST):
    pass


class CXXCompoundStatement(CompoundAST, AST):
    pass


class CCompoundStatement(CStatement, CXXCompoundStatement, AST):
    pass


class CConcatenatedString(CExpression, AST):
    pass


class ConditionalAST(AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class IfAST(ControlFlowAST, ConditionalAST, AST):
    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore


class CXXConditionalExpression(IfAST, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class CConditionalExpression(CExpression, CXXConditionalExpression, AST):
    pass


class CConst(CAST, TerminalSymbol, AST):
    pass


class CContinue(CAST, TerminalSymbol, AST):
    pass


class CXXContinueStatement(AST):
    pass


class CContinueStatement(CStatement, CXXContinueStatement, AST):
    pass


class DeclarationAST(AST):
    pass


class VariableDeclarationAST(DeclarationAST, AST):
    pass


class CXXDeclaration(StatementAST, VariableDeclarationAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CDeclaration(CXXDeclaration, CAST, AST):
    pass


class CDeclarationList(CAST, AST):
    pass


class CDefault(CAST, TerminalSymbol, AST):
    pass


class CDefined(CAST, TerminalSymbol, AST):
    pass


class CDo(CAST, TerminalSymbol, AST):
    pass


class LoopAST(ControlFlowAST, AST):
    pass


class CXXDoStatement(LoopAST, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CDoStatement(CStatement, CXXDoStatement, AST):
    pass


class CElse(CAST, TerminalSymbol, AST):
    pass


class CXXEmptyStatement(AST):
    pass


class CEmptyStatement(CXXEmptyStatement, CAST, AST):
    pass


class CEnum(CAST, TerminalSymbol, AST):
    pass


class TypeDeclarationAST(DeclarationAST, AST):
    pass


class DefinitionAST(DeclarationAST, AST):
    pass


class CXXEnumSpecifier(DefinitionAST, TypeDeclarationAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CEnumSpecifier(CTypeSpecifier, CXXEnumSpecifier, AST):
    pass


class CEnumSpecifier0(CEnumSpecifier, AST):
    pass


class CEnumSpecifier1(CEnumSpecifier, AST):
    pass


class DegenerateDeclarationAST(AST):
    pass


class CTagSpecifier(AST):
    pass


class CEnumTagSpecifier(CEnumSpecifier, CTagSpecifier, DegenerateDeclarationAST, CAST, AST):
    pass


class CXXEnumerator(VariableDeclarationAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class CEnumerator(CXXEnumerator, CAST, AST):
    pass


class CEnumerator0(CEnumerator, AST):
    pass


class CEnumerator1(CEnumerator, AST):
    pass


class CXXEnumeratorList(AST):
    pass


class CEnumeratorList(CXXEnumeratorList, CAST, AST):
    pass


class CEnumeratorList0(CEnumeratorList, AST):
    pass


class CEnumeratorList1(CEnumeratorList, AST):
    pass


class CEnumeratorList2(CEnumeratorList, AST):
    pass


class CEnumeratorList3(CEnumeratorList, AST):
    pass


class ParseErrorAST(AST):
    pass


class CXXError(ParseErrorAST, AST):
    pass


class CError(CAST, CXXError, ParseErrorAST, AST):
    pass


class ErrorTree(ParseErrorAST, AST):
    pass


class CErrorTree(ErrorTree, CAST, AST):
    pass


class VariationPoint(AST):
    pass


class ErrorVariationPoint(VariationPoint, AST):
    pass


class CErrorVariationPoint(ErrorVariationPoint, CAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class CErrorVariationPointTree(ErrorVariationPoint, CAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class CEscapeSequence(CAST, AST):
    pass


class ExpressionStatementAST(StatementAST, AST):
    pass


class CXXExpressionStatement(ExpressionStatementAST, AST):
    pass


class CExpressionStatement(CStatement, CXXExpressionStatement, AST):
    pass


class CExpressionStatement0(CExpressionStatement, AST):
    pass


class CExpressionStatement1(CExpressionStatement, AST):
    pass


class CExtern(CAST, TerminalSymbol, AST):
    pass


class CFalse(CExpression, AST):
    pass


class CXXFieldDeclaration(DefinitionAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CFieldDeclaration(CXXFieldDeclaration, CAST, AST):
    pass


class CFieldDeclaration0(CFieldDeclaration, AST):
    pass


class CFieldDeclaration1(CFieldDeclaration, AST):
    pass


class CFieldDeclaration2(CFieldDeclaration, AST):
    pass


class CFieldDeclaration3(CFieldDeclaration, AST):
    pass


class CXXFieldDeclarationList(AST):
    pass


class CFieldDeclarationList(CXXFieldDeclarationList, CAST, AST):
    pass


class CFieldDesignator(CAST, AST):
    pass


class FieldAST(ExpressionAST, AST):
    pass


class CXXFieldExpression(FieldAST, AST):
    @_property
    def field(self) -> Optional[AST]:
        return self.child_slot("field")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class CFieldExpression(CExpression, CXXFieldExpression, AST):
    pass


class IdentifierAST(AST):
    pass


class CXXFieldIdentifier(IdentifierAST, AST):
    pass


class CFieldIdentifier(CFieldDeclarator, CXXFieldIdentifier, AST):
    pass


class CFor(CAST, TerminalSymbol, AST):
    pass


class CXXForStatement(LoopAST, AST):
    @_property
    def initializer(self) -> Optional[AST]:
        return self.child_slot("initializer")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def update(self) -> Optional[AST]:
        return self.child_slot("update")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CForStatement(CStatement, CXXForStatement, AST):
    pass


class CForStatement0(CForStatement, AST):
    pass


class CForStatement1(CForStatement, AST):
    pass


class CXXFunctionDeclarator(AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class CFunctionDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXFunctionDeclarator, AST):
    pass


class CFunctionDeclarator0(CFunctionDeclarator, AST):
    pass


class CFunctionDeclarator1(CFunctionDeclarator, AST):
    pass


class FunctionAST(AST):
    def function_name(self: "FunctionAST") -> str:
        """Return the function name of this AST."""
        return _interface.dispatch(FunctionAST.function_name.__name__, self)

    def function_parameters(self: "FunctionAST") -> List[AST]:
        """Return the function parameters of this AST."""
        return _interface.dispatch(FunctionAST.function_parameters.__name__, self) or []

    def function_body(self: "FunctionAST") -> AST:
        """Return the function body of this AST."""
        return _interface.dispatch(FunctionAST.function_body.__name__, self)


class FunctionDeclarationAST(FunctionAST, DeclarationAST, AST):
    pass


class CXXFunctionDefinition(DefinitionAST, FunctionDeclarationAST, StatementAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CFunctionDefinition(CXXFunctionDefinition, CAST, AST):
    pass


class CFunctionDefinition0(CFunctionDefinition, AST):
    pass


class CFunctionDefinition1(CFunctionDefinition, AST):
    pass


class CGoto(CAST, TerminalSymbol, AST):
    pass


class CGotoStatement(CStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore


class CXXIdentifier(IdentifierAST, AST):
    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CIdentifier(CDeclarator, CExpression, CXXIdentifier, AST):
    pass


class CIf(CAST, TerminalSymbol, AST):
    pass


class CXXIfStatement(IfAST, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class CIfStatement(CStatement, CXXIfStatement, AST):
    pass


class CIfStatement0(CIfStatement, AST):
    pass


class CIfStatement1(CIfStatement, AST):
    pass


class VariableInitializationAST(VariableDeclarationAST, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CXXInitDeclarator(VariableInitializationAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class CInitDeclarator(CXXInitDeclarator, CAST, AST):
    pass


class CInitializerList(CAST, AST):
    pass


class CInitializerList0(CInitializerList, AST):
    pass


class CInitializerList1(CInitializerList, AST):
    pass


class CInitializerList2(CInitializerList, AST):
    pass


class CInitializerList3(CInitializerList, AST):
    pass


class CXXInitializerPair(AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def designator(self) -> List[AST]:
        return self.child_slot("designator")  # type: ignore


class CInitializerPair(CXXInitializerPair, CAST, AST):
    pass


class CInline(CAST, TerminalSymbol, AST):
    pass


class InnerWhitespace(TextFragment, AST):
    pass


class CInnerWhitespace(CAST, InnerWhitespace, AST):
    pass


class CWcharDoubleQuote(CAST, TerminalSymbol, AST):
    pass


class CWcharSingleQuote(CAST, TerminalSymbol, AST):
    pass


class CLabeledStatement(CStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def statement(self) -> Optional[AST]:
        return self.child_slot("statement")  # type: ignore


class CLinkageSpecification(CAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CLong(CAST, TerminalSymbol, AST):
    pass


class MacroDeclarationAST(DeclarationAST, AST):
    @_property
    def define_terminal(self) -> Optional[AST]:
        return self.child_slot("define_terminal")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CXXMacroForwardDeclaration(MacroDeclarationAST, AST):
    pass


class CMacroForwardDeclaration(CStatement, CXXMacroForwardDeclaration, AST):
    pass


class CMacroTypeSpecifier(CTypeSpecifier, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CMsBasedModifier(CAST, AST):
    pass


class CMsCallModifier(CAST, AST):
    pass


class CMsDeclspecModifier(CAST, AST):
    pass


class CMsPointerModifier(CAST, AST):
    pass


class CMsRestrictModifier(CAST, AST):
    pass


class CMsSignedPtrModifier(CAST, AST):
    pass


class CMsUnalignedPtrModifier(CAST, AST):
    pass


class CMsUnsignedPtrModifier(CAST, AST):
    pass


class CNull(CExpression, AST):
    pass


class NumberAST(LiteralAST, AST):
    pass


class CXXNumberLiteral(NumberAST, AST):
    pass


class CNumberLiteral(CExpression, CXXNumberLiteral, AST):
    pass


class ParameterAST(VariableDeclarationAST, AST):
    pass


class CXXParameterDeclaration(ParameterAST, VariableDeclarationAST, AST):
    pass


class CParameterDeclaration(CXXParameterDeclaration, CAST, AST):
    pass


class CParameterDeclaration0(CParameterDeclaration, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CParameterDeclaration1(CParameterDeclaration, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class ParametersAST(AST):
    pass


class CXXParameterList(ParametersAST, AST):
    pass


class CParameterList(CXXParameterList, CAST, AST):
    pass


class CParameterList0(CParameterList, AST):
    pass


class CParameterList1(CParameterList, AST):
    pass


class CXXParenthesizedDeclarator(AST):
    pass


class CParenthesizedDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXParenthesizedDeclarator, AST):
    pass


class ParenthesizedExpressionAST(ExpressionAST, AST):
    pass


class CXXParenthesizedExpression(ParenthesizedExpressionAST, AST):
    pass


class CParenthesizedExpression(CExpression, CXXParenthesizedExpression, AST):
    pass


class CParenthesizedExpression0(CParenthesizedExpression, AST):
    pass


class CParenthesizedExpression1(CParenthesizedExpression, AST):
    pass


class CXXPointerDeclarator(AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CPointerDeclarator(CTypeDeclarator, CFieldDeclarator, CDeclarator, CXXPointerDeclarator, AST):
    pass


class CXXPointerExpression(AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class CPointerExpression(CExpression, CXXPointerExpression, AST):
    pass


class CXXPreprocArg(AST):
    pass


class CPreprocArg(CXXPreprocArg, CAST, AST):
    pass


class CPreprocCall(CAST, AST):
    @_property
    def directive(self) -> Optional[AST]:
        return self.child_slot("directive")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class CXXPreprocDef(DefinitionAST, MacroDeclarationAST, AST):
    pass


class CPreprocDef(CXXPreprocDef, CAST, AST):
    pass


class CPreprocDefined(CAST, AST):
    pass


class CPreprocDefined0(CPreprocDefined, AST):
    pass


class CPreprocDefined1(CPreprocDefined, AST):
    pass


class CPreprocDirective(CAST, AST):
    pass


class CXXPreprocElif(AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def elif_terminal(self) -> Optional[AST]:
        return self.child_slot("elif_terminal")  # type: ignore


class CPreprocElif(CXXPreprocElif, CAST, AST):
    pass


class CPreprocElif0(CPreprocElif, AST):
    pass


class CPreprocElif1(CPreprocElif, AST):
    pass


class CXXPreprocElse(AST):
    @_property
    def else_terminal(self) -> Optional[AST]:
        return self.child_slot("else_terminal")  # type: ignore


class CPreprocElse(CXXPreprocElse, CAST, AST):
    pass


class CPreprocElse0(CPreprocElse, AST):
    pass


class CPreprocElse1(CPreprocElse, AST):
    pass


class CXXPreprocFunctionDef(DefinitionAST, MacroDeclarationAST, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class CPreprocFunctionDef(CXXPreprocFunctionDef, CAST, AST):
    pass


class CXXPreprocIf(AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def if_terminal(self) -> Optional[AST]:
        return self.child_slot("if_terminal")  # type: ignore

    @_property
    def endif_terminal(self) -> Optional[AST]:
        return self.child_slot("endif_terminal")  # type: ignore


class CPreprocIf(CXXPreprocIf, CAST, AST):
    pass


class CPreprocIf0(CPreprocIf, AST):
    pass


class CPreprocIf1(CPreprocIf, AST):
    pass


class CXXPreprocIfdef(AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def if_terminal(self) -> Optional[AST]:
        return self.child_slot("if_terminal")  # type: ignore

    @_property
    def endif_terminal(self) -> Optional[AST]:
        return self.child_slot("endif_terminal")  # type: ignore


class CPreprocIfdef(CXXPreprocIfdef, CAST, AST):
    pass


class CPreprocIfdef0(CPreprocIfdef, AST):
    pass


class CPreprocIfdef1(CPreprocIfdef, AST):
    pass


class CXXPreprocInclude(AST):
    @_property
    def include_terminal(self) -> Optional[AST]:
        return self.child_slot("include_terminal")  # type: ignore

    @_property
    def path(self) -> Optional[AST]:
        return self.child_slot("path")  # type: ignore


class CPreprocInclude(CXXPreprocInclude, CAST, AST):
    pass


class CXXPreprocParams(AST):
    pass


class CPreprocParams(CXXPreprocParams, CAST, AST):
    pass


class TypeAST(AST):
    pass


class CXXPrimitiveType(TypeAST, AST):
    pass


class CPrimitiveType(CTypeSpecifier, CXXPrimitiveType, AST):
    pass


class CRegister(CAST, TerminalSymbol, AST):
    pass


class CRestrict(CAST, TerminalSymbol, AST):
    pass


class CReturn(CAST, TerminalSymbol, AST):
    pass


class ReturnAST(StatementAST, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class CXXReturnStatement(ReturnAST, AST):
    pass


class CReturnStatement(CStatement, CXXReturnStatement, AST):
    pass


class CReturnStatement0(CReturnStatement, AST):
    pass


class CReturnStatement1(CReturnStatement, AST):
    pass


class CShort(CAST, TerminalSymbol, AST):
    pass


class CXXSigned(AST):
    pass


class CSigned(CXXSigned, CAST, TerminalSymbol, AST):
    pass


class CXXSizedTypeSpecifier(TypeAST, AST):
    @_property
    def modifiers(self) -> List[AST]:
        return self.child_slot("modifiers")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CSizedTypeSpecifier(CTypeSpecifier, CXXSizedTypeSpecifier, AST):
    pass


class CSizeof(CAST, TerminalSymbol, AST):
    pass


class CXXSizeofExpression(AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class CSizeofExpression(CExpression, CXXSizeofExpression, AST):
    pass


class CSizeofExpression0(CSizeofExpression, AST):
    pass


class CSizeofExpression1(CSizeofExpression, AST):
    pass


class SourceTextFragment(AST):
    pass


class CSourceTextFragment(CAST, SourceTextFragment, AST):
    pass


class CSourceTextFragmentTree(ErrorTree, CAST, AST):
    pass


class SourceTextFragmentVariationPoint(VariationPoint, AST):
    pass


class CSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, CAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class CSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, CAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class CStatementIdentifier(CAST, AST):
    pass


class CStatic(CAST, TerminalSymbol, AST):
    pass


class CXXStorageClassSpecifier(AST):
    pass


class CStorageClassSpecifier(CXXStorageClassSpecifier, CAST, AST):
    pass


class StringAST(LiteralAST, AST):
    pass


class CXXStringLiteral(StringAST, AST):
    pass


class CStringLiteral(CExpression, CXXStringLiteral, AST):
    pass


class CStruct(CAST, TerminalSymbol, AST):
    pass


class ClassAST(TypeDeclarationAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CXXClassoidSpecifier(ClassAST, AST):
    pass


class CompositeTypeAST(AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CXXStructSpecifier(CompositeTypeAST, DefinitionAST, TypeDeclarationAST, AST):
    pass


class CStructSpecifier(CTypeSpecifier, CXXStructSpecifier, CXXClassoidSpecifier, AST):
    pass


class CStructSpecifier0(CStructSpecifier, AST):
    pass


class CStructSpecifier1(CStructSpecifier, AST):
    pass


class CStructSpecifier2(CStructSpecifier, AST):
    pass


class CStructSpecifier3(CStructSpecifier, AST):
    pass


class CStructSpecifier4(CStructSpecifier, AST):
    pass


class CStructTagSpecifier(CStructSpecifier, CTagSpecifier, DegenerateDeclarationAST, CAST, AST):
    pass


class CSubscriptDesignator(CAST, AST):
    pass


class SubscriptAST(AST):
    pass


class CXXSubscriptExpression(SubscriptAST, AST):
    @_property
    def index(self) -> Optional[AST]:
        return self.child_slot("index")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class CSubscriptExpression(CExpression, CXXSubscriptExpression, AST):
    pass


class CSwitch(CAST, TerminalSymbol, AST):
    pass


class CXXSwitchStatement(ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class CSwitchStatement(CStatement, CXXSwitchStatement, AST):
    pass


class CXXSystemLibString(AST):
    pass


class CSystemLibString(CXXSystemLibString, CAST, AST):
    pass


class RootAST(AST):
    pass


class CXXTranslationUnit(RootAST, AST):
    pass


class CTranslationUnit(CXXTranslationUnit, CAST, AST):
    pass


class CTrue(CExpression, AST):
    pass


class CXXTypeDefinition(DefinitionAST, TypeDeclarationAST, AST):
    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CTypeDefinition(CXXTypeDefinition, CAST, AST):
    pass


class CXXTypeDescriptor(TypeAST, AST):
    @_property
    def post_type_qualifiers(self) -> List[AST]:
        return self.child_slot("post_type_qualifiers")  # type: ignore

    @_property
    def pre_type_qualifiers(self) -> List[AST]:
        return self.child_slot("pre_type_qualifiers")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CTypeDescriptor(CXXTypeDescriptor, CAST, AST):
    pass


class CXXTypeForwardDeclaration(TypeDeclarationAST, AST):
    pass


class CTypeForwardDeclaration(CStatement, CXXTypeForwardDeclaration, AST):
    pass


class TypeIdentifierAST(IdentifierAST, TypeAST, AST):
    pass


class CXXTypeIdentifier(TypeIdentifierAST, AST):
    pass


class CTypeIdentifier(CTypeDeclarator, CTypeSpecifier, CXXTypeIdentifier, AST):
    pass


class CXXTypeQualifier(AST):
    pass


class CTypeQualifier(CXXTypeQualifier, CAST, AST):
    pass


class CTypedef(CAST, TerminalSymbol, AST):
    pass


class CUnicodeDoubleQuote(CAST, TerminalSymbol, AST):
    pass


class CUnsignedTerminalDoubleQuote(CAST, TerminalSymbol, AST):
    pass


class CUnicodeSingleQuote(CAST, TerminalSymbol, AST):
    pass


class CUnsignedTerminalSingleQuote(CAST, TerminalSymbol, AST):
    pass


class CUnsigned8bitTerminalDoubleQuote(CAST, TerminalSymbol, AST):
    pass


class CUnsigned8bitTerminalSingleQuote(CAST, TerminalSymbol, AST):
    pass


class UnaryAST(ExpressionAST, AST):
    pass


class CXXUnaryExpression(UnaryAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class CUnaryExpression(CExpression, CXXUnaryExpression, AST):
    pass


class CUnion(CAST, TerminalSymbol, AST):
    pass


class CXXUnionSpecifier(CompositeTypeAST, DefinitionAST, TypeDeclarationAST, AST):
    pass


class CUnionSpecifier(CTypeSpecifier, CXXUnionSpecifier, CXXClassoidSpecifier, AST):
    pass


class CUnionSpecifier0(CUnionSpecifier, AST):
    pass


class CUnionSpecifier1(CUnionSpecifier, AST):
    pass


class CUnionSpecifier2(CUnionSpecifier, AST):
    pass


class CUnionSpecifier3(CUnionSpecifier, AST):
    pass


class CUnionSpecifier4(CUnionSpecifier, AST):
    pass


class CUnionTagSpecifier(CUnionSpecifier, CTagSpecifier, DegenerateDeclarationAST, CAST, AST):
    pass


class CUnsigned(CAST, TerminalSymbol, AST):
    pass


class CXXUpdateExpression(AssignmentAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class CUpdateExpression(CExpression, CXXUpdateExpression, AST):
    pass


class CUpdateExpressionPostfix(CUpdateExpression, AST):
    pass


class CUpdateExpressionPrefix(CUpdateExpression, AST):
    pass


class CVariadicDeclaration(CParameterDeclaration, CIdentifier, AST):
    pass


class CVariadicParameter(CAST, AST):
    pass


class CVolatile(CAST, TerminalSymbol, AST):
    pass


class CWhile(CAST, TerminalSymbol, AST):
    pass


class WhileAST(ControlFlowAST, ConditionalAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CXXWhileStatement(LoopAST, WhileAST, AST):
    pass


class CWhileStatement(CStatement, CXXWhileStatement, AST):
    pass


class COpenBracket(CAST, TerminalSymbol, AST):
    pass


class COpenAttribute(CAST, TerminalSymbol, AST):
    pass


class CCloseBracket(CAST, TerminalSymbol, AST):
    pass


class CCloseAttribute(CAST, TerminalSymbol, AST):
    pass


class CXXBitwiseXor(AST):
    pass


class CBitwiseXor(CXXBitwiseXor, CAST, TerminalSymbol, AST):
    pass


class CBitwiseXorAssign(CAST, TerminalSymbol, AST):
    pass


class COpenBrace(CAST, TerminalSymbol, AST):
    pass


class CXXBitwiseOr(AST):
    pass


class CBitwiseOr(CXXBitwiseOr, CAST, TerminalSymbol, AST):
    pass


class CBitwiseOrAssign(CAST, TerminalSymbol, AST):
    pass


class CXXLogicalOr(AST):
    pass


class CLogicalOr(CXXLogicalOr, CAST, TerminalSymbol, AST):
    pass


class CCloseBrace(CAST, TerminalSymbol, AST):
    pass


class CXXBitwiseNot(AST):
    pass


class CBitwiseNot(CXXBitwiseNot, CAST, TerminalSymbol, AST):
    pass


class CPPAST(CXXAST, CLikeSyntaxAST, NormalScopeAST, AST):
    pass


class CPPNewline(CPPAST, TerminalSymbol, AST):
    pass


class CPPLogicalNot(CXXLogicalNot, CPPAST, TerminalSymbol, AST):
    pass


class CPPNotEqual(CXXNotEqual, CPPAST, TerminalSymbol, AST):
    pass


class CPPDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPEmptyString(CPPAST, TerminalSymbol, AST):
    pass


class CPPMacroDefine(CXXMacroDefine, CPPAST, AST):
    pass


class CPPMacroElif(CXXMacroElif, CPPAST, AST):
    pass


class CPPMacroElse(CXXMacroElse, CPPAST, AST):
    pass


class CPPMacroEndIf(CXXMacroEndIf, CPPAST, AST):
    pass


class CPPMacroIf(CXXMacroIf, CPPAST, AST):
    pass


class CPPMacroIfDefined(CXXMacroIfDefined, CPPAST, AST):
    pass


class CPPMacroIfNotDefined(CXXMacroIfNotDefined, CPPAST, AST):
    pass


class CPPMacroInclude(CXXMacroInclude, CPPAST, AST):
    pass


class CPPModulo(CXXModulo, CPPAST, TerminalSymbol, AST):
    pass


class CPPModuleAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseAnd(CXXBitwiseAnd, CPPAST, TerminalSymbol, AST):
    pass


class CPPLogicalAnd(CXXLogicalAnd, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseAndAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPSingleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPOpenParenthesis(CPPAST, TerminalSymbol, AST):
    pass


class CPPCallOperator(CPPAST, TerminalSymbol, AST):
    pass


class CPPCloseParenthesis(CPPAST, TerminalSymbol, AST):
    pass


class CPPMultiply(CXXMultiply, CPPAST, TerminalSymbol, AST):
    pass


class CPPMultiplyAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPAdd(CXXAdd, CPPAST, TerminalSymbol, AST):
    pass


class CPPIncrement(CXXIncrement, CPPAST, TerminalSymbol, AST):
    pass


class CPPAddAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPComma(CPPAST, TerminalSymbol, AST):
    pass


class CPPSubtract(CXXSubtract, CPPAST, TerminalSymbol, AST):
    pass


class CPPDecrement(CXXDecrement, CPPAST, TerminalSymbol, AST):
    pass


class CPPAttributeSubtract(CPPAST, TerminalSymbol, AST):
    pass


class CPPBased(CPPAST, TerminalSymbol, AST):
    pass


class CPPCdecl(CPPAST, TerminalSymbol, AST):
    pass


class CPPClrcall(CPPAST, TerminalSymbol, AST):
    pass


class CPPDeclspec(CPPAST, TerminalSymbol, AST):
    pass


class CPPFastcall(CPPAST, TerminalSymbol, AST):
    pass


class CPPStdcall(CPPAST, TerminalSymbol, AST):
    pass


class CPPThiscall(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnderscoreUnaligned(CPPAST, TerminalSymbol, AST):
    pass


class CPPVectorcall(CPPAST, TerminalSymbol, AST):
    pass


class CPPSubtractAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPDashArrow(CXXDashArrow, CPPAST, TerminalSymbol, AST):
    pass


class CPPPointerToMemberArrow(CPPAST, TerminalSymbol, AST):
    pass


class CPPAbstractDeclarator(CPPAST, AST):
    pass


class CPPAtomic(CPPAST, TerminalSymbol, AST):
    pass


class CPPDeclarator(CXXDeclarator, CPPAST, AST):
    pass


class CPPExpression(CXXExpression, CPPAST, AST):
    pass


class CPPFieldDeclarator(CPPAST, AST):
    pass


class CPPStatement(CXXStatement, CPPAST, AST):
    pass


class CPPTypeDeclarator(CPPAST, AST):
    pass


class CPPTypeSpecifier(CPPAST, AST):
    pass


class CPPUnaligned(CPPAST, TerminalSymbol, AST):
    pass


class CPPDot(CPPAST, TerminalSymbol, AST):
    pass


class CPPPointerToMemberDot(CPPAST, TerminalSymbol, AST):
    pass


class CPPEllipsis(CPPAST, TerminalSymbol, AST):
    pass


class CPPDivide(CXXDivide, CPPAST, TerminalSymbol, AST):
    pass


class CPPDivideAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPColon(CPPAST, TerminalSymbol, AST):
    pass


class CPPScopeResolution(CPPAST, TerminalSymbol, AST):
    pass


class CPPSemicolon(CPPAST, TerminalSymbol, AST):
    pass


class CPPLessThan(CXXLessThan, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitshiftLeft(CXXBitshiftLeft, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitshiftLeftAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPLessThanOrEqual(CXXLessThanOrEqual, CPPAST, TerminalSymbol, AST):
    pass


class CPPSpaceship(CPPAST, TerminalSymbol, AST):
    pass


class CPPAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPEqual(CXXEqual, CPPAST, TerminalSymbol, AST):
    pass


class CPPGreaterThan(CXXGreaterThan, CPPAST, TerminalSymbol, AST):
    pass


class CPPGreaterThanOrEqual(CXXGreaterThanOrEqual, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitshiftRight(CXXBitshiftRight, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitshiftRightAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPQuestion(CPPAST, TerminalSymbol, AST):
    pass


class CPPAbstractArrayDeclarator(CPPAbstractDeclarator, CXXAbstractArrayDeclarator, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CPPAbstractFunctionDeclarator(CPPAbstractDeclarator, CXXAbstractFunctionDeclarator, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CPPAbstractFunctionDeclarator0(CPPAbstractFunctionDeclarator, AST):
    pass


class CPPAbstractFunctionDeclarator1(CPPAbstractFunctionDeclarator, AST):
    pass


class CPPAbstractFunctionDeclarator2(CPPAbstractFunctionDeclarator, AST):
    pass


class CPPAbstractFunctionDeclarator3(CPPAbstractFunctionDeclarator, AST):
    pass


class CPPAbstractParenthesizedDeclarator(CPPAbstractDeclarator, AST):
    pass


class CPPAbstractPointerDeclarator(CPPAbstractDeclarator, CXXAbstractPointerDeclarator, AST):
    pass


class CPPAbstractReferenceDeclarator(CPPAbstractDeclarator, AST):
    pass


class CPPAbstractReferenceDeclarator0(CPPAbstractReferenceDeclarator, AST):
    pass


class CPPAbstractReferenceDeclarator1(CPPAbstractReferenceDeclarator, AST):
    pass


class CPPAccessSpecifier(CPPAST, AST):
    @_property
    def keyword(self) -> Optional[AST]:
        return self.child_slot("keyword")  # type: ignore


class CPPAliasDeclaration(TypeDeclarationAST, CPPAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CPPArgumentList(CXXArgumentList, CPPAST, AST):
    pass


class CPPArgumentList0(CPPArgumentList, AST):
    pass


class CPPArgumentList1(CPPArgumentList, AST):
    pass


class CPPArrayDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXArrayDeclarator, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CPPAssignmentExpression(CPPExpression, CXXAssignmentExpression, AST):
    pass


class CPPAttribute(CPPAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def prefix(self) -> Optional[AST]:
        return self.child_slot("prefix")  # type: ignore


class CPPAttribute0(CPPAttribute, AST):
    pass


class CPPAttribute1(CPPAttribute, AST):
    pass


class CPPAttribute2(CPPAttribute, AST):
    pass


class CPPAttribute3(CPPAttribute, AST):
    pass


class CPPAttributeDeclaration(CPPAST, AST):
    pass


class CPPAttributeSpecifier(CPPAST, AST):
    pass


class CPPAttributedDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, AST):
    pass


class CPPAttributedStatement(CPPAST, AST):
    pass


class CPPAttributedStatement0(CPPAttributedStatement, AST):
    pass


class CPPAttributedStatement1(CPPAttributedStatement, AST):
    pass


class CPPAuto(CPPAST, AST):
    pass


class CPPBaseClassClause(CPPAST, AST):
    pass


class CPPBaseClassClause0(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause1(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause10(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause11(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause2(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause3(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause4(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause5(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause6(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause7(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause8(CPPBaseClassClause, AST):
    pass


class CPPBaseClassClause9(CPPBaseClassClause, AST):
    pass


class CPPBinaryExpression(CPPExpression, CXXBinaryExpression, AST):
    pass


class CPPBinaryExpression0(CPPBinaryExpression, AST):
    pass


class CPPBinaryExpression1(CPPBinaryExpression, AST):
    pass


class CPPBitfieldClause(CPPAST, AST):
    pass


class CPPBlot(CPPAST, Blot, AST):
    pass


class CPPBreak(CPPAST, TerminalSymbol, AST):
    pass


class CPPBreakStatement(CPPStatement, CXXBreakStatement, AST):
    pass


class CPPCallExpression(CPPExpression, CXXCallExpression, AST):
    pass


class CPPCase(CPPAST, TerminalSymbol, AST):
    pass


class CPPCaseStatement(CPPStatement, CXXCaseStatement, AST):
    pass


class CPPCaseStatement0(CPPCaseStatement, AST):
    pass


class CPPCaseStatement1(CPPCaseStatement, AST):
    pass


class CPPCastExpression(CPPExpression, CXXCastExpression, AST):
    pass


class CPPCatch(CPPAST, TerminalSymbol, AST):
    pass


class CatchAST(StatementAST, AST):
    pass


class CPPCatchClause(CatchAST, CPPAST, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CPPCharLiteral(CPPExpression, CXXCharLiteral, AST):
    pass


class CPPClass(CPPAST, TerminalSymbol, AST):
    pass


class CPPClassSpecifier(CPPTypeSpecifier, CXXClassoidSpecifier, CompositeTypeAST, TypeDeclarationAST, DefinitionAST, AST):
    pass


class CPPClassSpecifier0(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier1(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier10(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier11(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier12(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier13(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier14(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier15(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier16(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier17(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier18(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier19(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier2(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier20(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier21(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier22(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier23(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier24(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier25(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier26(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier27(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier28(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier29(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier3(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier30(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier31(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier32(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier33(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier34(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier35(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier4(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier5(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier6(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier7(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier8(CPPClassSpecifier, AST):
    pass


class CPPClassSpecifier9(CPPClassSpecifier, AST):
    pass


class CPPCoAwait(CPPAST, TerminalSymbol, AST):
    pass


class CPPCoAwaitExpression(CPPExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class CPPCoReturn(CPPAST, TerminalSymbol, AST):
    pass


class CPPCoReturnStatement(CPPStatement, AST):
    pass


class CPPCoReturnStatement0(CPPCoReturnStatement, AST):
    pass


class CPPCoReturnStatement1(CPPCoReturnStatement, AST):
    pass


class CPPCoYield(CPPAST, TerminalSymbol, AST):
    pass


class CPPCoYieldStatement(CPPStatement, AST):
    pass


class CPPCommaExpression(CXXCommaExpression, CPPAST, AST):
    pass


class CPPComment(CXXComment, CPPAST, AST):
    pass


class CPPCompoundLiteralExpression(CPPExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CPPCompoundLiteralExpression0(CPPCompoundLiteralExpression, AST):
    pass


class CPPCompoundLiteralExpression1(CPPCompoundLiteralExpression, AST):
    pass


class CPPCompoundRequirement(CPPAST, AST):
    pass


class CPPCompoundRequirement0(CPPCompoundRequirement, AST):
    pass


class CPPCompoundRequirement1(CPPCompoundRequirement, AST):
    pass


class CPPCompoundRequirement2(CPPCompoundRequirement, AST):
    pass


class CPPCompoundRequirement3(CPPCompoundRequirement, AST):
    pass


class CPPCompoundStatement(CPPStatement, CXXCompoundStatement, AST):
    pass


class CPPConcatenatedString(CPPExpression, AST):
    pass


class CPPConcept(CPPAST, TerminalSymbol, AST):
    pass


class CPPConceptDefinition(CPPAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CXXConditionClause(AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def initializer(self) -> Optional[AST]:
        return self.child_slot("initializer")  # type: ignore


class CPPConditionClause(CXXConditionClause, CPPAST, AST):
    pass


class CPPConditionClause0(CPPConditionClause, AST):
    pass


class CPPConditionClause1(CPPConditionClause, AST):
    pass


class CPPConditionalExpression(CPPExpression, CXXConditionalExpression, AST):
    pass


class CPPConst(CPPAST, TerminalSymbol, AST):
    pass


class CPPConsteval(CPPAST, TerminalSymbol, AST):
    pass


class CPPConstexpr(CPPAST, TerminalSymbol, AST):
    pass


class CPPConstinit(CPPAST, TerminalSymbol, AST):
    pass


class CPPConstraintConjunction(CPPAST, AST):
    @_property
    def left(self) -> List[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> List[AST]:
        return self.child_slot("right")  # type: ignore


class CPPConstraintConjunction0(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction1(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction10(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction11(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction12(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction13(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction14(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction15(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction16(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction17(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction18(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction19(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction2(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction20(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction21(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction22(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction23(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction24(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction3(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction4(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction5(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction6(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction7(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction8(CPPConstraintConjunction, AST):
    pass


class CPPConstraintConjunction9(CPPConstraintConjunction, AST):
    pass


class CPPConstraintDisjunction(CPPAST, AST):
    @_property
    def left(self) -> List[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> List[AST]:
        return self.child_slot("right")  # type: ignore


class CPPConstraintDisjunction0(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction1(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction10(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction11(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction12(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction13(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction14(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction15(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction16(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction17(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction18(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction19(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction2(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction20(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction21(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction22(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction23(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction24(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction3(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction4(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction5(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction6(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction7(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction8(CPPConstraintDisjunction, AST):
    pass


class CPPConstraintDisjunction9(CPPConstraintDisjunction, AST):
    pass


class CPPContinue(CPPAST, TerminalSymbol, AST):
    pass


class CPPContinueStatement(CPPStatement, CXXContinueStatement, AST):
    pass


class CPPDeclaration(CXXDeclaration, CPPAST, AST):
    pass


class CPPDeclaration0(CPPDeclaration, AST):
    pass


class CPPDeclaration1(CPPDeclaration, AST):
    pass


class CPPDeclaration2(CPPDeclaration, AST):
    pass


class CPPDeclaration3(CPPDeclaration, AST):
    pass


class CPPDeclarationList(CPPAST, AST):
    pass


class CPPDecltype(CPPTypeSpecifier, AST):
    pass


class CPPDecltypeTerminal(CPPTypeSpecifier, TerminalSymbol, AST):
    pass


class CPPDefault(CPPAST, TerminalSymbol, AST):
    pass


class CPPDefaultMethodClause(CPPAST, AST):
    pass


class CPPDefined(CPPAST, TerminalSymbol, AST):
    pass


class CPPDelete(CPPAST, TerminalSymbol, AST):
    pass


class CPPDeleteExpression(CPPExpression, AST):
    pass


class CPPDeleteExpression0(CPPDeleteExpression, AST):
    pass


class CPPDeleteExpression1(CPPDeleteExpression, AST):
    pass


class CPPDeleteMethodClause(CPPAST, AST):
    pass


class CPPDependentName(CPPAST, AST):
    pass


class CPPDependentType(CPPTypeSpecifier, AST):
    pass


class CPPDestructorName(CPPDeclarator, AST):
    pass


class CPPDo(CPPAST, TerminalSymbol, AST):
    pass


class CPPDoStatement(CPPStatement, CXXDoStatement, AST):
    pass


class CPPElse(CPPAST, TerminalSymbol, AST):
    pass


class CPPEmptyStatement(CXXEmptyStatement, CPPAST, AST):
    pass


class CPPEnum(CPPAST, TerminalSymbol, AST):
    pass


class CPPEnumSpecifier(CPPTypeSpecifier, CXXEnumSpecifier, AST):
    @_property
    def scope(self) -> Optional[AST]:
        return self.child_slot("scope")  # type: ignore

    @_property
    def base(self) -> Optional[AST]:
        return self.child_slot("base")  # type: ignore


class CPPEnumSpecifier0(CPPEnumSpecifier, AST):
    pass


class CPPEnumSpecifier1(CPPEnumSpecifier, AST):
    pass


class CPPEnumSpecifier2(CPPEnumSpecifier, AST):
    pass


class CPPEnumSpecifier3(CPPEnumSpecifier, AST):
    pass


class CPPEnumSpecifier4(CPPEnumSpecifier, AST):
    pass


class CPPEnumerator(CXXEnumerator, CPPAST, AST):
    pass


class CPPEnumerator0(CPPEnumerator, AST):
    pass


class CPPEnumerator1(CPPEnumerator, AST):
    pass


class CPPEnumeratorList(CXXEnumeratorList, CPPAST, AST):
    pass


class CPPEnumeratorList0(CPPEnumeratorList, AST):
    pass


class CPPEnumeratorList1(CPPEnumeratorList, AST):
    pass


class CPPEnumeratorList2(CPPEnumeratorList, AST):
    pass


class CPPEnumeratorList3(CPPEnumeratorList, AST):
    pass


class CPPError(CPPAST, CXXError, ParseErrorAST, AST):
    pass


class CPPErrorTree(ErrorTree, CPPAST, AST):
    pass


class CPPErrorVariationPoint(ErrorVariationPoint, CPPAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class CPPErrorVariationPointTree(ErrorVariationPoint, CPPAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class CPPEscapeSequence(CPPAST, AST):
    pass


class CPPExplicit(CPPAST, TerminalSymbol, AST):
    pass


class CPPExplicitFunctionSpecifier(CPPAST, AST):
    pass


class CPPExplicitFunctionSpecifier0(CPPExplicitFunctionSpecifier, AST):
    pass


class CPPExplicitFunctionSpecifier1(CPPExplicitFunctionSpecifier, AST):
    pass


class CPPExpressionStatement(CPPStatement, CXXExpressionStatement, AST):
    pass


class CPPExpressionStatement0(CPPExpressionStatement, AST):
    pass


class CPPExpressionStatement1(CPPExpressionStatement, AST):
    pass


class CPPExtern(CPPAST, TerminalSymbol, AST):
    pass


class CPPFalse(CPPExpression, AST):
    pass


class CPPFieldDeclaration(CXXFieldDeclaration, CPPAST, AST):
    @_property
    def default_value(self) -> Optional[AST]:
        return self.child_slot("default_value")  # type: ignore


class CPPFieldDeclaration0(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration1(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration2(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration3(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration4(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration5(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration6(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclaration7(CPPFieldDeclaration, AST):
    pass


class CPPFieldDeclarationList(CXXFieldDeclarationList, CPPAST, AST):
    pass


class CPPFieldDesignator(CPPAST, AST):
    pass


class CPPFieldExpression(CPPExpression, CXXFieldExpression, AST):
    pass


class CPPFieldIdentifier(CPPFieldDeclarator, CXXFieldIdentifier, AST):
    pass


class CPPFieldInitializer(CPPAST, AST):
    pass


class CPPFieldInitializer0(CPPFieldInitializer, AST):
    pass


class CPPFieldInitializer1(CPPFieldInitializer, AST):
    pass


class CPPFieldInitializer2(CPPFieldInitializer, AST):
    pass


class CPPFieldInitializerList(CPPAST, AST):
    pass


class CPPFinal(CPPAST, TerminalSymbol, AST):
    pass


class CPPFoldExpression(CPPExpression, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class CPPFoldExpression0(CPPFoldExpression, AST):
    pass


class CPPFoldExpression1(CPPFoldExpression, AST):
    pass


class CPPFoldExpression10(CPPFoldExpression, AST):
    pass


class CPPFoldExpression11(CPPFoldExpression, AST):
    pass


class CPPFoldExpression12(CPPFoldExpression, AST):
    pass


class CPPFoldExpression13(CPPFoldExpression, AST):
    pass


class CPPFoldExpression14(CPPFoldExpression, AST):
    pass


class CPPFoldExpression15(CPPFoldExpression, AST):
    pass


class CPPFoldExpression16(CPPFoldExpression, AST):
    pass


class CPPFoldExpression17(CPPFoldExpression, AST):
    pass


class CPPFoldExpression18(CPPFoldExpression, AST):
    pass


class CPPFoldExpression19(CPPFoldExpression, AST):
    pass


class CPPFoldExpression2(CPPFoldExpression, AST):
    pass


class CPPFoldExpression20(CPPFoldExpression, AST):
    pass


class CPPFoldExpression21(CPPFoldExpression, AST):
    pass


class CPPFoldExpression22(CPPFoldExpression, AST):
    pass


class CPPFoldExpression23(CPPFoldExpression, AST):
    pass


class CPPFoldExpression24(CPPFoldExpression, AST):
    pass


class CPPFoldExpression25(CPPFoldExpression, AST):
    pass


class CPPFoldExpression26(CPPFoldExpression, AST):
    pass


class CPPFoldExpression27(CPPFoldExpression, AST):
    pass


class CPPFoldExpression28(CPPFoldExpression, AST):
    pass


class CPPFoldExpression29(CPPFoldExpression, AST):
    pass


class CPPFoldExpression3(CPPFoldExpression, AST):
    pass


class CPPFoldExpression30(CPPFoldExpression, AST):
    pass


class CPPFoldExpression31(CPPFoldExpression, AST):
    pass


class CPPFoldExpression32(CPPFoldExpression, AST):
    pass


class CPPFoldExpression4(CPPFoldExpression, AST):
    pass


class CPPFoldExpression5(CPPFoldExpression, AST):
    pass


class CPPFoldExpression6(CPPFoldExpression, AST):
    pass


class CPPFoldExpression7(CPPFoldExpression, AST):
    pass


class CPPFoldExpression8(CPPFoldExpression, AST):
    pass


class CPPFoldExpression9(CPPFoldExpression, AST):
    pass


class CPPFor(CPPAST, TerminalSymbol, AST):
    pass


class CPPForRangeLoop(CPPStatement, LoopAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CPPForStatement(CPPStatement, CXXForStatement, AST):
    pass


class CPPForStatement0(CPPForStatement, AST):
    pass


class CPPForStatement1(CPPForStatement, AST):
    pass


class CPPFriend(CPPAST, TerminalSymbol, AST):
    pass


class CPPFriendDeclaration(CPPAST, AST):
    pass


class CPPFriendDeclaration0(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration1(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration10(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration11(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration12(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration2(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration3(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration4(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration5(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration6(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration7(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration8(CPPFriendDeclaration, AST):
    pass


class CPPFriendDeclaration9(CPPFriendDeclaration, AST):
    pass


class CPPFunctionDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXFunctionDeclarator, AST):
    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore


class CPPFunctionDeclarator0(CPPFunctionDeclarator, AST):
    pass


class CPPFunctionDeclarator1(CPPFunctionDeclarator, AST):
    pass


class CPPFunctionDeclarator2(CPPFunctionDeclarator, AST):
    pass


class CPPFunctionDefinition(CXXFunctionDefinition, CPPAST, AST):
    pass


class CPPFunctionDefinition0(CPPFunctionDefinition, AST):
    pass


class CPPFunctionDefinition1(CPPFunctionDefinition, AST):
    pass


class CPPFunctionDefinition2(CPPFunctionDefinition, AST):
    pass


class CPPFunctionDefinition3(CPPFunctionDefinition, AST):
    pass


class CPPGoto(CPPAST, TerminalSymbol, AST):
    pass


class CPPGotoStatement(CPPStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore


class CPPIdentifier(CPPDeclarator, CPPExpression, CXXIdentifier, AST):
    pass


class CPPIf(CPPAST, TerminalSymbol, AST):
    pass


class CPPIfStatement(CPPStatement, CXXIfStatement, AST):
    pass


class CPPIfStatement0(CPPIfStatement, AST):
    pass


class CPPIfStatement1(CPPIfStatement, AST):
    pass


class CPPIfStatement2(CPPIfStatement, AST):
    pass


class CPPIfStatement3(CPPIfStatement, AST):
    pass


class CPPInitDeclarator(CXXInitDeclarator, CPPAST, AST):
    pass


class CPPInitDeclarator0(CPPInitDeclarator, AST):
    pass


class CPPInitDeclarator1(CPPInitDeclarator, AST):
    pass


class CPPInitializerList(CPPAST, AST):
    pass


class CPPInitializerList0(CPPInitializerList, AST):
    pass


class CPPInitializerList1(CPPInitializerList, AST):
    pass


class CPPInitializerList2(CPPInitializerList, AST):
    pass


class CPPInitializerList3(CPPInitializerList, AST):
    pass


class CPPInitializerPair(CXXInitializerPair, CPPAST, AST):
    pass


class CPPInline(CPPAST, TerminalSymbol, AST):
    pass


class CPPInnerWhitespace(CPPAST, InnerWhitespace, AST):
    pass


class CPPWcharDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPWcharSingleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPLabeledStatement(CPPStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def statement(self) -> Optional[AST]:
        return self.child_slot("statement")  # type: ignore


class CPPLambdaCaptureSpecifier(CPPAST, AST):
    pass


class CPPLambdaCaptureSpecifier0(CPPLambdaCaptureSpecifier, AST):
    pass


class CPPLambdaCaptureSpecifier1(CPPLambdaCaptureSpecifier, AST):
    pass


class CPPLambdaCaptureSpecifier2(CPPLambdaCaptureSpecifier, AST):
    pass


class CPPLambdaCaptureSpecifier3(CPPLambdaCaptureSpecifier, AST):
    pass


class CPPLambdaDefaultCapture(CPPAST, AST):
    pass


class CPPLambdaExpression(CPPExpression, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def constraint(self) -> Optional[AST]:
        return self.child_slot("constraint")  # type: ignore

    @_property
    def template_parameters(self) -> Optional[AST]:
        return self.child_slot("template_parameters")  # type: ignore

    @_property
    def captures(self) -> Optional[AST]:
        return self.child_slot("captures")  # type: ignore


class CPPLambdaExpression0(CPPLambdaExpression, AST):
    pass


class CPPLambdaExpression1(CPPLambdaExpression, AST):
    pass


class CPPLambdaExpression2(CPPLambdaExpression, AST):
    pass


class CPPLambdaExpression3(CPPLambdaExpression, AST):
    pass


class CPPLambdaExpression4(CPPLambdaExpression, AST):
    pass


class CPPLambdaExpression5(CPPLambdaExpression, AST):
    pass


class CPPLinkageSpecification(CPPAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CPPLiteralSuffix(CPPAST, AST):
    pass


class CPPLong(CPPAST, TerminalSymbol, AST):
    pass


class CPPMacroForwardDeclaration(CPPStatement, CXXMacroForwardDeclaration, AST):
    pass


class CPPMsBasedModifier(CPPAST, AST):
    pass


class CPPMsCallModifier(CPPAST, AST):
    pass


class CPPMsDeclspecModifier(CPPAST, AST):
    pass


class CPPMsPointerModifier(CPPAST, AST):
    pass


class CPPMsRestrictModifier(CPPAST, AST):
    pass


class CPPMsSignedPtrModifier(CPPAST, AST):
    pass


class CPPMsUnalignedPtrModifier(CPPAST, AST):
    pass


class CPPMsUnsignedPtrModifier(CPPAST, AST):
    pass


class CPPMutable(CPPAST, TerminalSymbol, AST):
    pass


class CPPNamespace(CPPAST, TerminalSymbol, AST):
    pass


class CPPNamespaceAliasDefinition(CPPAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class NamespaceDeclarationAST(DeclarationAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CPPNamespaceDefinition(NamespaceDeclarationAST, DefinitionAST, CPPAST, AST):
    pass


class CPPNamespaceDefinitionName(CPPAST, AST):
    pass


class CPPNamespaceDefinitionName0(CPPNamespaceDefinitionName, AST):
    pass


class CPPNamespaceDefinitionName1(CPPNamespaceDefinitionName, AST):
    pass


class CPPNamespaceIdentifier(IdentifierAST, CPPAST, AST):
    pass


class CPPNew(CPPAST, TerminalSymbol, AST):
    pass


class CPPNewDeclarator(CPPAST, AST):
    @_property
    def length(self) -> Optional[AST]:
        return self.child_slot("length")  # type: ignore


class CPPNewDeclarator0(CPPNewDeclarator, AST):
    pass


class CPPNewDeclarator1(CPPNewDeclarator, AST):
    pass


class CPPNewExpression(CPPExpression, AST):
    @_property
    def placement(self) -> Optional[AST]:
        return self.child_slot("placement")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class CPPNoexcept(CPPAST, AST):
    pass


class CPPNoexcept0(CPPNoexcept, AST):
    pass


class CPPNoexcept1(CPPNoexcept, AST):
    pass


class CPPNoexcept2(CPPNoexcept, AST):
    pass


class CPPNoexceptTerminal(CPPAST, TerminalSymbol, AST):
    pass


class CPPNull(CPPExpression, AST):
    pass


class CPPNullptr(CPPExpression, AST):
    pass


class CPPNumberLiteral(CPPExpression, CXXNumberLiteral, AST):
    pass


class CPPOperator(CPPAST, TerminalSymbol, AST):
    pass


class CPPOperatorCast(CPPAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CPPOperatorName(CPPFieldDeclarator, CPPDeclarator, IdentifierAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def array(self) -> Optional[AST]:
        return self.child_slot("array")  # type: ignore

    @_property
    def suffix_identifier(self) -> Optional[AST]:
        return self.child_slot("suffix_identifier")  # type: ignore


class CPPOperatorName0(CPPOperatorName, AST):
    pass


class CPPOperatorName1(CPPOperatorName, AST):
    pass


class CPPOperatorName2(CPPOperatorName, AST):
    pass


class CPPOptionalParameterDeclaration(ParameterAST, VariableInitializationAST, VariableDeclarationAST, CPPAST, AST):
    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def default_value(self) -> Optional[AST]:
        return self.child_slot("default_value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CPPOptionalTypeParameterDeclaration(ParameterAST, CPPAST, AST):
    @_property
    def default_type(self) -> Optional[AST]:
        return self.child_slot("default_type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CPPOptionalTypeParameterDeclaration0(CPPOptionalTypeParameterDeclaration, AST):
    pass


class CPPOptionalTypeParameterDeclaration1(CPPOptionalTypeParameterDeclaration, AST):
    pass


class CPPOverride(CPPAST, TerminalSymbol, AST):
    pass


class CPPParameterDeclaration(CXXParameterDeclaration, CPPAST, AST):
    pass


class CPPParameterDeclaration0(CPPParameterDeclaration, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CPPParameterDeclaration1(CPPParameterDeclaration, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CPPParameterList(CXXParameterList, CPPAST, AST):
    pass


class CPPParameterPackExpansion(CPPExpression, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class CPPParenthesizedDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXParenthesizedDeclarator, AST):
    pass


class CPPParenthesizedExpression(CPPExpression, CXXParenthesizedExpression, AST):
    pass


class CPPParenthesizedExpression0(CPPParenthesizedExpression, AST):
    pass


class CPPParenthesizedExpression1(CPPParenthesizedExpression, AST):
    pass


class CPPPlaceholderTypeSpecifier(CPPTypeSpecifier, AST):
    @_property
    def constraint(self) -> Optional[AST]:
        return self.child_slot("constraint")  # type: ignore


class CPPPlaceholderTypeSpecifier0(CPPPlaceholderTypeSpecifier, AST):
    pass


class CPPPlaceholderTypeSpecifier1(CPPPlaceholderTypeSpecifier, AST):
    pass


class CPPPointerDeclarator(CPPTypeDeclarator, CPPFieldDeclarator, CPPDeclarator, CXXPointerDeclarator, AST):
    pass


class CPPPointerExpression(CPPExpression, CXXPointerExpression, AST):
    pass


class CPPPreprocArg(CXXPreprocArg, CPPAST, AST):
    pass


class CPPPreprocCall(CPPAST, AST):
    @_property
    def directive(self) -> Optional[AST]:
        return self.child_slot("directive")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class CPPPreprocDef(CXXPreprocDef, CPPAST, AST):
    pass


class CPPPreprocDefined(CPPAST, AST):
    pass


class CPPPreprocDefined0(CPPPreprocDefined, AST):
    pass


class CPPPreprocDefined1(CPPPreprocDefined, AST):
    pass


class CPPPreprocDirective(CPPAST, AST):
    pass


class CPPPreprocElif(CXXPreprocElif, CPPAST, AST):
    pass


class CPPPreprocElif0(CPPPreprocElif, AST):
    pass


class CPPPreprocElif1(CPPPreprocElif, AST):
    pass


class CPPPreprocElse(CXXPreprocElse, CPPAST, AST):
    pass


class CPPPreprocElse0(CPPPreprocElse, AST):
    pass


class CPPPreprocElse1(CPPPreprocElse, AST):
    pass


class CPPPreprocFunctionDef(CXXPreprocFunctionDef, CPPAST, AST):
    pass


class CPPPreprocIf(CXXPreprocIf, CPPAST, AST):
    pass


class CPPPreprocIf0(CPPPreprocIf, AST):
    pass


class CPPPreprocIf1(CPPPreprocIf, AST):
    pass


class CPPPreprocIfdef(CXXPreprocIfdef, CPPAST, AST):
    pass


class CPPPreprocIfdef0(CPPPreprocIfdef, AST):
    pass


class CPPPreprocIfdef1(CPPPreprocIfdef, AST):
    pass


class CPPPreprocInclude(CXXPreprocInclude, CPPAST, AST):
    pass


class CPPPreprocParams(CXXPreprocParams, CPPAST, AST):
    pass


class CPPPrimitiveType(CPPTypeSpecifier, CXXPrimitiveType, IdentifierAST, AST):
    pass


class CPPPrivate(CPPAST, TerminalSymbol, AST):
    pass


class CPPProtected(CPPAST, TerminalSymbol, AST):
    pass


class CPPPublic(CPPAST, TerminalSymbol, AST):
    pass


class CPPQualifiedIdentifier(CPPDeclarator, CPPTypeSpecifier, CPPExpression, IdentifierAST, AST):
    @_property
    def scope(self) -> Optional[AST]:
        return self.child_slot("scope")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class CPPRawStringLiteral(CPPExpression, StringAST, AST):
    pass


class CPPRefQualifier(CPPAST, AST):
    pass


class CPPReferenceDeclarator(CPPFieldDeclarator, CPPDeclarator, AST):
    @_property
    def valueness(self) -> Optional[AST]:
        return self.child_slot("valueness")  # type: ignore


class CPPRegister(CPPAST, TerminalSymbol, AST):
    pass


class CPPRequirementSeq(CPPAST, AST):
    pass


class CPPRequires(CPPAST, TerminalSymbol, AST):
    pass


class CPPRequiresClause(CPPExpression, AST):
    @_property
    def constraint(self) -> List[AST]:
        return self.child_slot("constraint")  # type: ignore


class CPPRequiresClause0(CPPRequiresClause, AST):
    pass


class CPPRequiresClause1(CPPRequiresClause, AST):
    pass


class CPPRequiresClause2(CPPRequiresClause, AST):
    pass


class CPPRequiresClause3(CPPRequiresClause, AST):
    pass


class CPPRequiresClause4(CPPRequiresClause, AST):
    pass


class CPPRequiresExpression(CPPExpression, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def requirements(self) -> Optional[AST]:
        return self.child_slot("requirements")  # type: ignore


class CPPRestrict(CPPAST, TerminalSymbol, AST):
    pass


class CPPReturn(CPPAST, TerminalSymbol, AST):
    pass


class CPPReturnStatement(CPPStatement, CXXReturnStatement, AST):
    pass


class CPPReturnStatement0(CPPReturnStatement, AST):
    pass


class CPPReturnStatement1(CPPReturnStatement, AST):
    pass


class CPPReturnStatement2(CPPReturnStatement, AST):
    pass


class CPPShort(CPPAST, TerminalSymbol, AST):
    pass


class CPPSigned(CXXSigned, CPPAST, TerminalSymbol, AST):
    pass


class CPPSimpleRequirement(CPPAST, AST):
    pass


class CPPSizedTypeSpecifier(CPPTypeSpecifier, CXXSizedTypeSpecifier, AST):
    pass


class CPPSizeof(CPPAST, TerminalSymbol, AST):
    pass


class CPPSizeofExpression(CPPExpression, CXXSizeofExpression, AST):
    pass


class CPPSizeofExpression0(CPPSizeofExpression, AST):
    pass


class CPPSizeofExpression1(CPPSizeofExpression, AST):
    pass


class CPPSourceTextFragment(CPPAST, SourceTextFragment, AST):
    pass


class CPPSourceTextFragmentTree(ErrorTree, CPPAST, AST):
    pass


class CPPSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, CPPAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class CPPSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, CPPAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class CPPStatementIdentifier(CPPAST, AST):
    pass


class CPPStatic(CPPAST, TerminalSymbol, AST):
    pass


class CPPStaticAssert(CPPAST, TerminalSymbol, AST):
    pass


class CPPStaticAssertDeclaration(CPPAST, AST):
    @_property
    def message(self) -> Optional[AST]:
        return self.child_slot("message")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class CPPStaticAssertDeclaration0(CPPStaticAssertDeclaration, AST):
    pass


class CPPStaticAssertDeclaration1(CPPStaticAssertDeclaration, AST):
    pass


class CPPStorageClassSpecifier(CXXStorageClassSpecifier, CPPAST, AST):
    pass


class CPPStringLiteral(CPPExpression, CXXStringLiteral, AST):
    pass


class CPPStruct(CPPAST, TerminalSymbol, AST):
    pass


class CPPStructSpecifier(CPPTypeSpecifier, CXXStructSpecifier, CXXClassoidSpecifier, AST):
    pass


class CPPStructSpecifier0(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier1(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier10(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier11(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier12(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier13(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier14(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier15(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier16(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier17(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier18(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier19(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier2(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier20(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier21(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier22(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier23(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier24(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier25(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier26(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier27(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier28(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier29(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier3(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier30(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier31(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier32(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier33(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier34(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier35(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier4(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier5(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier6(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier7(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier8(CPPStructSpecifier, AST):
    pass


class CPPStructSpecifier9(CPPStructSpecifier, AST):
    pass


class CPPStructuredBindingDeclarator(CPPDeclarator, AST):
    pass


class CPPSubscriptDesignator(CPPAST, AST):
    pass


class CPPSubscriptExpression(CPPExpression, CXXSubscriptExpression, AST):
    pass


class CPPSwitch(CPPAST, TerminalSymbol, AST):
    pass


class CPPSwitchStatement(CPPStatement, CXXSwitchStatement, AST):
    pass


class CPPSystemLibString(CXXSystemLibString, CPPAST, AST):
    pass


class CPPTemplate(CPPAST, TerminalSymbol, AST):
    pass


class CPPTemplateArgumentList(CPPAST, AST):
    pass


class CPPTemplateArgumentList0(CPPTemplateArgumentList, AST):
    pass


class CPPTemplateArgumentList1(CPPTemplateArgumentList, AST):
    pass


class CPPTemplateArgumentList2(CPPTemplateArgumentList, AST):
    pass


class CPPTemplateDeclaration(CPPAST, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class CPPTemplateDeclaration0(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration1(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration2(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration3(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration4(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration5(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration6(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration7(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration8(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateDeclaration9(CPPTemplateDeclaration, AST):
    pass


class CPPTemplateFunction(CPPDeclarator, CPPExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class CPPTemplateInstantiation(CPPAST, AST):
    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class CPPTemplateInstantiation0(CPPTemplateInstantiation, AST):
    pass


class CPPTemplateInstantiation1(CPPTemplateInstantiation, AST):
    pass


class CPPTemplateMethod(CPPFieldDeclarator, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class CPPTemplateParameterList(ParametersAST, CPPAST, AST):
    pass


class CPPTemplateParameterList0(CPPTemplateParameterList, AST):
    pass


class CPPTemplateParameterList1(CPPTemplateParameterList, AST):
    pass


class CPPTemplateTemplateParameterDeclaration(ParameterAST, CPPAST, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class CPPTemplateType(CPPTypeSpecifier, TypeAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class CPPThis(CPPExpression, AST):
    pass


class CPPThreadLocal(CPPAST, TerminalSymbol, AST):
    pass


class CPPThrow(CPPAST, TerminalSymbol, AST):
    pass


class CPPThrowSpecifier(CPPAST, AST):
    pass


class CPPThrowSpecifier0(CPPThrowSpecifier, AST):
    pass


class CPPThrowSpecifier1(CPPThrowSpecifier, AST):
    pass


class CPPThrowStatement(CPPStatement, AST):
    pass


class CPPThrowStatement0(CPPThrowStatement, AST):
    pass


class CPPThrowStatement1(CPPThrowStatement, AST):
    pass


class CPPTrailingReturnType(CPPAST, AST):
    pass


class CPPTranslationUnit(CXXTranslationUnit, CPPAST, AST):
    pass


class CPPTrue(CPPExpression, AST):
    pass


class CPPTry(CPPAST, TerminalSymbol, AST):
    pass


class CPPTryStatement(CPPStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class CPPTypeDefinition(CXXTypeDefinition, CPPAST, AST):
    pass


class CPPTypeDescriptor(CXXTypeDescriptor, CPPAST, AST):
    pass


class CPPTypeForwardDeclaration(CPPStatement, CXXTypeForwardDeclaration, AST):
    pass


class CPPTypeIdentifier(CPPTypeDeclarator, CPPTypeSpecifier, CXXTypeIdentifier, IdentifierAST, AST):
    pass


class CPPTypeParameterDeclaration(ParameterAST, CPPAST, AST):
    @_property
    def keyword(self) -> Optional[AST]:
        return self.child_slot("keyword")  # type: ignore


class CPPTypeParameterDeclaration0(CPPTypeParameterDeclaration, AST):
    pass


class CPPTypeParameterDeclaration1(CPPTypeParameterDeclaration, AST):
    pass


class CPPTypeQualifier(CXXTypeQualifier, CPPAST, AST):
    pass


class CPPTypeRequirement(CPPAST, AST):
    pass


class CPPTypeRequirement0(CPPTypeRequirement, AST):
    pass


class CPPTypeRequirement1(CPPTypeRequirement, AST):
    pass


class CPPTypeRequirement2(CPPTypeRequirement, AST):
    pass


class CPPTypedef(CPPAST, TerminalSymbol, AST):
    pass


class CPPTypename(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnicodeDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnsignedTerminalDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnicodeSingleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnsignedTerminalSingleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnsigned8bitTerminalDoubleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnsigned8bitTerminalSingleQuote(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnaryExpression(CPPExpression, CXXUnaryExpression, AST):
    pass


class CPPUnion(CPPAST, TerminalSymbol, AST):
    pass


class CPPUnionSpecifier(CPPTypeSpecifier, CXXUnionSpecifier, CXXClassoidSpecifier, AST):
    pass


class CPPUnionSpecifier0(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier1(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier10(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier11(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier12(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier13(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier14(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier15(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier16(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier17(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier18(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier19(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier2(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier20(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier21(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier22(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier23(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier24(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier25(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier26(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier27(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier28(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier29(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier3(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier30(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier31(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier32(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier33(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier34(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier35(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier4(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier5(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier6(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier7(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier8(CPPUnionSpecifier, AST):
    pass


class CPPUnionSpecifier9(CPPUnionSpecifier, AST):
    pass


class CPPUnsigned(CPPAST, TerminalSymbol, AST):
    pass


class CPPUpdateExpression(CPPExpression, CXXUpdateExpression, AST):
    pass


class CPPUpdateExpressionPostfix(CPPUpdateExpression, AST):
    pass


class CPPUpdateExpressionPrefix(CPPUpdateExpression, AST):
    pass


class CPPUserDefinedLiteral(CPPExpression, AST):
    pass


class CPPUsing(CPPAST, TerminalSymbol, AST):
    pass


class CPPUsingDeclaration(CPPAST, AST):
    pass


class CPPUsingDeclaration0(CPPUsingDeclaration, AST):
    pass


class CPPUsingDeclaration1(CPPUsingDeclaration, AST):
    pass


class CPPVariadicDeclaration(CPPParameterDeclaration, CPPIdentifier, AST):
    pass


class CPPVariadicDeclarator(CPPAST, AST):
    pass


class CPPVariadicDeclarator0(CPPVariadicDeclarator, AST):
    pass


class CPPVariadicDeclarator1(CPPVariadicDeclarator, AST):
    pass


class CPPVariadicParameterDeclaration(ParameterAST, VariableDeclarationAST, CPPAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def declarator(self) -> Optional[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def pre_specifiers(self) -> List[AST]:
        return self.child_slot("pre_specifiers")  # type: ignore

    @_property
    def post_specifiers(self) -> List[AST]:
        return self.child_slot("post_specifiers")  # type: ignore


class CPPVariadicTypeParameterDeclaration(ParameterAST, CPPAST, AST):
    pass


class CPPVariadicTypeParameterDeclaration0(CPPVariadicTypeParameterDeclaration, AST):
    pass


class CPPVariadicTypeParameterDeclaration1(CPPVariadicTypeParameterDeclaration, AST):
    pass


class CPPVirtual(CPPAST, TerminalSymbol, AST):
    pass


class CPPVirtualFunctionSpecifier(CPPAST, AST):
    pass


class CPPVirtualSpecifier(CPPAST, AST):
    pass


class CPPVolatile(CPPAST, TerminalSymbol, AST):
    pass


class CPPWhile(CPPAST, TerminalSymbol, AST):
    pass


class CPPWhileStatement(CPPStatement, CXXWhileStatement, AST):
    pass


class CPPOpenBracket(CPPAST, TerminalSymbol, AST):
    pass


class CPPOpenAttribute(CPPAST, TerminalSymbol, AST):
    pass


class CPPEmptyCaptureClause(CPPAST, TerminalSymbol, AST):
    pass


class CPPCloseBracket(CPPAST, TerminalSymbol, AST):
    pass


class CPPCloseAttribute(CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseXor(CXXBitwiseXor, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseXorAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPOpenBrace(CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseOr(CXXBitwiseOr, CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseOrAssign(CPPAST, TerminalSymbol, AST):
    pass


class CPPLogicalOr(CXXLogicalOr, CPPAST, TerminalSymbol, AST):
    pass


class CPPCloseBrace(CPPAST, TerminalSymbol, AST):
    pass


class CPPBitwiseNot(CXXBitwiseNot, CPPAST, TerminalSymbol, AST):
    pass


class InnerParent(AST):
    pass


class JavaAST(CLikeSyntaxAST, AST):
    pass


class JavaLogicalNot(JavaAST, TerminalSymbol, AST):
    pass


class JavaNotEqual(JavaAST, TerminalSymbol, AST):
    pass


class JavaModulo(JavaAST, TerminalSymbol, AST):
    pass


class JavaModuleAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseAnd(JavaAST, TerminalSymbol, AST):
    pass


class JavaLogicalAnd(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseAndAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaOpenParenthesis(JavaAST, TerminalSymbol, AST):
    pass


class JavaCloseParenthesis(JavaAST, TerminalSymbol, AST):
    pass


class JavaMultiply(JavaAST, TerminalSymbol, AST):
    pass


class JavaMultiplyAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaAdd(JavaAST, TerminalSymbol, AST):
    pass


class JavaIncrement(JavaAST, TerminalSymbol, AST):
    pass


class JavaAddAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaComma(JavaAST, TerminalSymbol, AST):
    pass


class JavaSubtract(JavaAST, TerminalSymbol, AST):
    pass


class JavaDecrement(JavaAST, TerminalSymbol, AST):
    pass


class JavaSubtractAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaDashArrow(JavaAST, TerminalSymbol, AST):
    pass


class JavaExpression(ExpressionAST, JavaAST, AST):
    pass


class JavaPrimaryExpression(JavaExpression, AST):
    pass


class JavaLiteral(JavaPrimaryExpression, AST):
    pass


class JavaType(JavaAST, AST):
    @_property
    def element(self) -> Optional[AST]:
        return self.child_slot("element")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore


class JavaUnannotatedType(JavaType, AST):
    pass


class JavaSimpleType(JavaUnannotatedType, AST):
    pass


class JavaDot(JavaAST, TerminalSymbol, AST):
    pass


class JavaEllipsis(JavaAST, TerminalSymbol, AST):
    pass


class JavaDivide(JavaAST, TerminalSymbol, AST):
    pass


class JavaDivideAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaColon(JavaAST, TerminalSymbol, AST):
    pass


class JavaScopeResolution(JavaAST, TerminalSymbol, AST):
    pass


class JavaSemicolon(JavaAST, TerminalSymbol, AST):
    pass


class JavaLessThan(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitshiftLeft(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitshiftLeftAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaLessThanOrEqual(JavaAST, TerminalSymbol, AST):
    pass


class JavaAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaEqual(JavaAST, TerminalSymbol, AST):
    pass


class JavaGreaterThan(JavaAST, TerminalSymbol, AST):
    pass


class JavaGreaterThanOrEqual(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitshiftRight(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitshiftRightAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaUnsignedBitshiftRight(JavaAST, TerminalSymbol, AST):
    pass


class JavaUnsignedBitshiftRightAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaQuestion(JavaAST, TerminalSymbol, AST):
    pass


class JavaMatrixMultiply(JavaAST, TerminalSymbol, AST):
    pass


class JavaAtInterface(JavaAST, TerminalSymbol, AST):
    pass


class JavaAbstract(JavaAST, TerminalSymbol, AST):
    pass


class JavaAnnotatedType(JavaType, AST):
    pass


class JavaAnnotation(JavaAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class JavaAnnotationArgumentList(JavaAST, AST):
    pass


class JavaAnnotationArgumentList0(JavaAnnotationArgumentList, AST):
    pass


class JavaAnnotationArgumentList1(JavaAnnotationArgumentList, AST):
    pass


class JavaAnnotationArgumentList2(JavaAnnotationArgumentList, AST):
    pass


class JavaAnnotationArgumentList3(JavaAnnotationArgumentList, AST):
    pass


class JavaAnnotationTypeBody(JavaAST, AST):
    pass


class JavaStatement(StatementAST, JavaAST, AST):
    pass


class JavaDeclaration(JavaStatement, AST):
    pass


class JavaAnnotationTypeDeclaration(JavaDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaAnnotationTypeDeclaration0(JavaAnnotationTypeDeclaration, AST):
    pass


class JavaAnnotationTypeDeclaration1(JavaAnnotationTypeDeclaration, AST):
    pass


class JavaAnnotationTypeElementDeclaration(JavaAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaAnnotationTypeElementDeclaration0(JavaAnnotationTypeElementDeclaration, AST):
    pass


class JavaAnnotationTypeElementDeclaration1(JavaAnnotationTypeElementDeclaration, AST):
    pass


class JavaAnnotationTypeElementDeclaration2(JavaAnnotationTypeElementDeclaration, AST):
    pass


class JavaAnnotationTypeElementDeclaration3(JavaAnnotationTypeElementDeclaration, AST):
    pass


class JavaArgumentList(ArgumentsAST, JavaAST, AST):
    pass


class JavaArgumentList0(JavaArgumentList, AST):
    pass


class JavaArgumentList1(JavaArgumentList, AST):
    pass


class JavaArrayAccess(JavaPrimaryExpression, AST):
    @_property
    def array(self) -> Optional[AST]:
        return self.child_slot("array")  # type: ignore

    @_property
    def index(self) -> Optional[AST]:
        return self.child_slot("index")  # type: ignore


class JavaArrayCreationExpression(JavaPrimaryExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def dimensions(self) -> List[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaArrayCreationExpression0(JavaArrayCreationExpression, AST):
    pass


class JavaArrayCreationExpression1(JavaArrayCreationExpression, AST):
    pass


class JavaArrayInitializer(JavaAST, AST):
    pass


class JavaArrayInitializer0(JavaArrayInitializer, AST):
    pass


class JavaArrayInitializer1(JavaArrayInitializer, AST):
    pass


class JavaArrayInitializer2(JavaArrayInitializer, AST):
    pass


class JavaArrayInitializer3(JavaArrayInitializer, AST):
    pass


class JavaArrayType(JavaUnannotatedType, AST):
    pass


class JavaAssert(JavaAST, TerminalSymbol, AST):
    pass


class JavaAssertStatement(JavaStatement, AST):
    pass


class JavaAssertStatement0(JavaAssertStatement, AST):
    pass


class JavaAssertStatement1(JavaAssertStatement, AST):
    pass


class JavaAssignmentExpression(JavaExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavaAsterisk(JavaAST, AST):
    pass


class JavaBinaryExpression(JavaExpression, BinaryAST, AST):
    pass


class JavaBinaryIntegerLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaBlock(JavaStatement, AST):
    pass


class JavaComment(CommentAST, JavaAST, AST):
    pass


class JavaBlockComment(JavaComment, AST):
    pass


class JavaBlot(JavaAST, Blot, AST):
    pass


class JavaBooleanType(JavaSimpleType, AST):
    pass


class JavaBreak(JavaAST, TerminalSymbol, AST):
    pass


class JavaBreakStatement(JavaStatement, AST):
    pass


class JavaBreakStatement0(JavaBreakStatement, AST):
    pass


class JavaBreakStatement1(JavaBreakStatement, AST):
    pass


class JavaByte(JavaAST, TerminalSymbol, AST):
    pass


class JavaCase(JavaAST, TerminalSymbol, AST):
    pass


class JavaCastExpression(JavaExpression, AST):
    @_property
    def type(self) -> List[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class JavaCatch(JavaAST, TerminalSymbol, AST):
    pass


class JavaCatchClause(CatchAST, JavaAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavaCatchFormalParameter(JavaAST, AST):
    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaCatchFormalParameter0(JavaCatchFormalParameter, AST):
    pass


class JavaCatchFormalParameter1(JavaCatchFormalParameter, AST):
    pass


class JavaCatchType(JavaAST, AST):
    pass


class JavaChar(JavaAST, TerminalSymbol, AST):
    pass


class JavaCharacterLiteral(JavaLiteral, AST):
    pass


class JavaClass(JavaAST, TerminalSymbol, AST):
    pass


class JavaClassBody(JavaAST, AST):
    pass


class JavaClassDeclaration(JavaDeclaration, ClassAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def superclass(self) -> Optional[AST]:
        return self.child_slot("superclass")  # type: ignore

    @_property
    def interfaces(self) -> Optional[AST]:
        return self.child_slot("interfaces")  # type: ignore

    @_property
    def permits(self) -> Optional[AST]:
        return self.child_slot("permits")  # type: ignore


class JavaClassDeclaration0(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration1(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration10(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration11(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration12(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration13(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration14(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration15(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration16(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration17(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration18(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration19(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration2(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration20(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration21(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration22(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration23(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration24(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration25(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration26(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration27(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration28(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration29(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration3(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration30(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration31(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration4(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration5(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration6(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration7(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration8(JavaClassDeclaration, AST):
    pass


class JavaClassDeclaration9(JavaClassDeclaration, AST):
    pass


class JavaClassLiteral(JavaPrimaryExpression, LiteralAST, AST):
    pass


class JavaConstantDeclaration(JavaAST, AST):
    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaConstantDeclaration0(JavaConstantDeclaration, AST):
    pass


class JavaConstantDeclaration1(JavaConstantDeclaration, AST):
    pass


class JavaConstructorBody(JavaAST, AST):
    pass


class JavaConstructorBody0(JavaConstructorBody, AST):
    pass


class JavaConstructorBody1(JavaConstructorBody, AST):
    pass


class JavaConstructorDeclaration(JavaAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore


class JavaConstructorDeclaration0(JavaConstructorDeclaration, AST):
    pass


class JavaConstructorDeclaration1(JavaConstructorDeclaration, AST):
    pass


class JavaConstructorDeclaration2(JavaConstructorDeclaration, AST):
    pass


class JavaConstructorDeclaration3(JavaConstructorDeclaration, AST):
    pass


class JavaContinue(JavaAST, TerminalSymbol, AST):
    pass


class JavaContinueStatement(JavaStatement, AST):
    pass


class JavaContinueStatement0(JavaContinueStatement, AST):
    pass


class JavaContinueStatement1(JavaContinueStatement, AST):
    pass


class JavaDecimalFloatingPointLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaDecimalIntegerLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaDefault(JavaAST, TerminalSymbol, AST):
    pass


class JavaDimensions(JavaAST, AST):
    pass


class JavaDimensionsExpr(JavaAST, AST):
    pass


class JavaDo(JavaAST, TerminalSymbol, AST):
    pass


class JavaDoStatement(JavaStatement, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class JavaDouble(JavaAST, TerminalSymbol, AST):
    pass


class JavaElementValueArrayInitializer(JavaAST, AST):
    pass


class JavaElementValueArrayInitializer0(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValueArrayInitializer1(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValueArrayInitializer2(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValueArrayInitializer3(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValueArrayInitializer4(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValueArrayInitializer5(JavaElementValueArrayInitializer, AST):
    pass


class JavaElementValuePair(JavaAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class JavaElse(JavaAST, TerminalSymbol, AST):
    pass


class JavaEmptyStatement(JavaStatement, AST):
    pass


class JavaEnhancedForStatement(JavaStatement, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaEnhancedForStatement0(JavaEnhancedForStatement, AST):
    pass


class JavaEnhancedForStatement1(JavaEnhancedForStatement, AST):
    pass


class JavaEnum(JavaAST, TerminalSymbol, AST):
    pass


class JavaEnumBody(JavaAST, AST):
    pass


class JavaEnumBody0(JavaEnumBody, AST):
    pass


class JavaEnumBody1(JavaEnumBody, AST):
    pass


class JavaEnumBody2(JavaEnumBody, AST):
    pass


class JavaEnumBody3(JavaEnumBody, AST):
    pass


class JavaEnumBody4(JavaEnumBody, AST):
    pass


class JavaEnumBody5(JavaEnumBody, AST):
    pass


class JavaEnumBody6(JavaEnumBody, AST):
    pass


class JavaEnumBody7(JavaEnumBody, AST):
    pass


class JavaEnumBodyDeclarations(JavaAST, AST):
    pass


class JavaEnumConstant(JavaAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaEnumConstant0(JavaEnumConstant, AST):
    pass


class JavaEnumConstant1(JavaEnumConstant, AST):
    pass


class JavaEnumDeclaration(JavaDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def interfaces(self) -> Optional[AST]:
        return self.child_slot("interfaces")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaEnumDeclaration0(JavaEnumDeclaration, AST):
    pass


class JavaEnumDeclaration1(JavaEnumDeclaration, AST):
    pass


class JavaError(JavaAST, ParseErrorAST, AST):
    pass


class JavaErrorTree(ErrorTree, JavaAST, AST):
    pass


class JavaErrorVariationPoint(ErrorVariationPoint, JavaAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class JavaErrorVariationPointTree(ErrorVariationPoint, JavaAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class JavaExplicitConstructorInvocation(JavaAST, AST):
    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore

    @_property
    def constructor(self) -> Optional[AST]:
        return self.child_slot("constructor")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore


class JavaExplicitConstructorInvocation0(JavaExplicitConstructorInvocation, AST):
    pass


class JavaExplicitConstructorInvocation1(JavaExplicitConstructorInvocation, AST):
    pass


class JavaExports(JavaAST, TerminalSymbol, AST):
    pass


class JavaModuleDirective(JavaAST, AST):
    pass


class JavaExportsModuleDirective(JavaModuleDirective, AST):
    @_property
    def modules(self) -> List[AST]:
        return self.child_slot("modules")  # type: ignore

    @_property
    def package(self) -> Optional[AST]:
        return self.child_slot("package")  # type: ignore


class JavaExportsModuleDirective0(JavaExportsModuleDirective, AST):
    pass


class JavaExportsModuleDirective1(JavaExportsModuleDirective, AST):
    pass


class JavaExpressionStatement(JavaStatement, AST):
    pass


class JavaExtends(JavaAST, TerminalSymbol, AST):
    pass


class JavaExtendsInterfaces(JavaAST, AST):
    pass


class BooleanAST(LiteralAST, AST):
    pass


class BooleanFalseAST(BooleanAST, AST):
    pass


class JavaFalse(JavaLiteral, BooleanFalseAST, AST):
    pass


class FieldAsst(AST):
    @_property
    def field(self) -> Optional[AST]:
        return self.child_slot("field")  # type: ignore

    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore


class JavaFieldAccess(JavaPrimaryExpression, FieldAsst, AST):
    pass


class JavaFieldAccess0(JavaFieldAccess, AST):
    pass


class JavaFieldAccess1(JavaFieldAccess, AST):
    pass


class JavaFieldDeclaration(JavaAST, AST):
    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaFieldDeclaration0(JavaFieldDeclaration, AST):
    pass


class JavaFieldDeclaration1(JavaFieldDeclaration, AST):
    pass


class JavaFinal(JavaAST, TerminalSymbol, AST):
    pass


class JavaFinally(JavaAST, TerminalSymbol, AST):
    pass


class JavaFinallyClause(JavaAST, AST):
    pass


class JavaFloat(JavaAST, TerminalSymbol, AST):
    pass


class JavaFloatingPointType(JavaSimpleType, AST):
    pass


class JavaFor(JavaAST, TerminalSymbol, AST):
    pass


class JavaForStatement(JavaStatement, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def update(self) -> List[AST]:
        return self.child_slot("update")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def init(self) -> List[AST]:
        return self.child_slot("init")  # type: ignore


class JavaForStatement0(JavaForStatement, AST):
    pass


class JavaForStatement1(JavaForStatement, AST):
    pass


class JavaForStatement2(JavaForStatement, AST):
    pass


class JavaForStatement3(JavaForStatement, AST):
    pass


class JavaForStatement4(JavaForStatement, AST):
    pass


class JavaForStatement5(JavaForStatement, AST):
    pass


class JavaFormalParameter(JavaAST, AST):
    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaFormalParameter0(JavaFormalParameter, AST):
    pass


class JavaFormalParameter1(JavaFormalParameter, AST):
    pass


class JavaFormalParameters(JavaAST, AST):
    pass


class JavaFormalParameters0(JavaFormalParameters, AST):
    pass


class JavaFormalParameters1(JavaFormalParameters, AST):
    pass


class JavaFormalParameters2(JavaFormalParameters, AST):
    pass


class JavaFormalParameters3(JavaFormalParameters, AST):
    pass


class JavaGenericType(JavaSimpleType, TypeAST, AST):
    pass


class JavaGenericType0(JavaGenericType, AST):
    pass


class JavaGenericType1(JavaGenericType, AST):
    pass


class JavaHexFloatingPointLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaHexIntegerLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaIdentifier(JavaPrimaryExpression, IdentifierAST, AST):
    pass


class JavaIf(JavaAST, TerminalSymbol, AST):
    pass


class JavaIfStatement(JavaStatement, IfAST, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class JavaIfStatement0(JavaIfStatement, AST):
    pass


class JavaIfStatement1(JavaIfStatement, AST):
    pass


class JavaImplements(JavaAST, TerminalSymbol, AST):
    pass


class JavaImport(JavaAST, TerminalSymbol, AST):
    pass


class JavaImportDeclaration(JavaDeclaration, AST):
    pass


class JavaImportDeclaration0(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration1(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration2(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration3(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration4(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration5(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration6(JavaImportDeclaration, AST):
    pass


class JavaImportDeclaration7(JavaImportDeclaration, AST):
    pass


class JavaInferredParameters(JavaAST, AST):
    pass


class JavaInnerWhitespace(JavaAST, InnerWhitespace, AST):
    pass


class JavaInstanceof(JavaAST, TerminalSymbol, AST):
    pass


class JavaInstanceofExpression(JavaExpression, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavaInt(JavaAST, TerminalSymbol, AST):
    pass


class JavaIntegralType(JavaSimpleType, AST):
    pass


class JavaInterface(JavaAST, TerminalSymbol, AST):
    pass


class JavaInterfaceBody(JavaAST, AST):
    pass


class JavaInterfaceDeclaration(JavaDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def permits(self) -> Optional[AST]:
        return self.child_slot("permits")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaInterfaceDeclaration0(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration1(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration2(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration3(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration4(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration5(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration6(JavaInterfaceDeclaration, AST):
    pass


class JavaInterfaceDeclaration7(JavaInterfaceDeclaration, AST):
    pass


class JavaLabeledStatement(JavaStatement, AST):
    pass


class LambdaAST(FunctionAST, AST):
    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavaLambdaExpression(JavaExpression, LambdaAST, AST):
    pass


class JavaLineComment(JavaComment, AST):
    pass


class JavaLocalVariableDeclaration(JavaStatement, VariableDeclarationAST, AST):
    @_property
    def declarator(self) -> List[AST]:
        return self.child_slot("declarator")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaLocalVariableDeclaration0(JavaLocalVariableDeclaration, AST):
    pass


class JavaLocalVariableDeclaration1(JavaLocalVariableDeclaration, AST):
    pass


class JavaLong(JavaAST, TerminalSymbol, AST):
    pass


class JavaMarkerAnnotation(JavaAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaMethodDeclaration(JavaAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore


class JavaMethodDeclaration0(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration1(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration10(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration11(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration12(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration13(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration14(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration15(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration2(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration3(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration4(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration5(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration6(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration7(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration8(JavaMethodDeclaration, AST):
    pass


class JavaMethodDeclaration9(JavaMethodDeclaration, AST):
    pass


class JavaMethodInvocation(JavaPrimaryExpression, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class JavaMethodInvocation0(JavaMethodInvocation, AST):
    pass


class JavaMethodInvocation1(JavaMethodInvocation, AST):
    pass


class JavaMethodInvocation2(JavaMethodInvocation, AST):
    pass


class JavaMethodReference(JavaPrimaryExpression, AST):
    pass


class JavaMethodReference0(JavaMethodReference, AST):
    pass


class JavaMethodReference1(JavaMethodReference, AST):
    pass


class JavaMethodReference2(JavaMethodReference, AST):
    pass


class JavaMethodReference3(JavaMethodReference, AST):
    pass


class JavaModifiers(JavaAST, AST):
    @_property
    def modifiers(self) -> List[AST]:
        return self.child_slot("modifiers")  # type: ignore


class JavaModule(JavaAST, TerminalSymbol, AST):
    pass


class JavaModuleBody(JavaAST, AST):
    pass


class JavaModuleDeclaration(JavaDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def open(self) -> Optional[AST]:
        return self.child_slot("open")  # type: ignore


class JavaNative(JavaAST, TerminalSymbol, AST):
    pass


class JavaNew(JavaAST, TerminalSymbol, AST):
    pass


class JavaNonSealed(JavaAST, TerminalSymbol, AST):
    pass


class JavaNullLiteral(JavaLiteral, AST):
    pass


class JavaObjectCreationExpression(JavaPrimaryExpression, AST):
    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore


class JavaObjectCreationExpression0(JavaObjectCreationExpression, AST):
    pass


class JavaObjectCreationExpression1(JavaObjectCreationExpression, AST):
    pass


class JavaOctalIntegerLiteral(JavaLiteral, LiteralAST, AST):
    pass


class JavaOpen(JavaAST, TerminalSymbol, AST):
    pass


class JavaOpens(JavaAST, TerminalSymbol, AST):
    pass


class JavaOpensModuleDirective(JavaModuleDirective, AST):
    @_property
    def modules(self) -> List[AST]:
        return self.child_slot("modules")  # type: ignore

    @_property
    def package(self) -> Optional[AST]:
        return self.child_slot("package")  # type: ignore


class JavaOpensModuleDirective0(JavaOpensModuleDirective, AST):
    pass


class JavaOpensModuleDirective1(JavaOpensModuleDirective, AST):
    pass


class JavaPackage(JavaAST, TerminalSymbol, AST):
    pass


class JavaPackageDeclaration(JavaDeclaration, AST):
    pass


class JavaPackageDeclaration0(JavaPackageDeclaration, AST):
    pass


class JavaPackageDeclaration1(JavaPackageDeclaration, AST):
    pass


class JavaParenthesizedExpression(JavaPrimaryExpression, ParenthesizedExpressionAST, AST):
    pass


class JavaPermits(JavaAST, AST):
    pass


class JavaPermitsTerminal(JavaAST, TerminalSymbol, AST):
    pass


class JavaPrivate(JavaAST, TerminalSymbol, AST):
    pass


class JavaProgram(RootAST, JavaAST, AST):
    pass


class JavaProtected(JavaAST, TerminalSymbol, AST):
    pass


class JavaProvides(JavaAST, TerminalSymbol, AST):
    pass


class JavaProvidesModuleDirective(JavaModuleDirective, AST):
    @_property
    def provider(self) -> List[AST]:
        return self.child_slot("provider")  # type: ignore

    @_property
    def provided(self) -> Optional[AST]:
        return self.child_slot("provided")  # type: ignore


class JavaProvidesModuleDirective0(JavaProvidesModuleDirective, AST):
    pass


class JavaProvidesModuleDirective1(JavaProvidesModuleDirective, AST):
    pass


class JavaPublic(JavaAST, TerminalSymbol, AST):
    pass


class JavaReceiverParameter(JavaAST, AST):
    pass


class JavaReceiverParameter0(JavaReceiverParameter, AST):
    pass


class JavaReceiverParameter1(JavaReceiverParameter, AST):
    pass


class JavaRecord(JavaAST, TerminalSymbol, AST):
    pass


class JavaRecordDeclaration(JavaAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaRecordDeclaration0(JavaRecordDeclaration, AST):
    pass


class JavaRecordDeclaration1(JavaRecordDeclaration, AST):
    pass


class JavaRequires(JavaAST, TerminalSymbol, AST):
    pass


class JavaRequiresModifier(JavaAST, AST):
    pass


class JavaRequiresModuleDirective(JavaModuleDirective, AST):
    @_property
    def modifiers(self) -> List[AST]:
        return self.child_slot("modifiers")  # type: ignore

    @_property
    def module(self) -> Optional[AST]:
        return self.child_slot("module")  # type: ignore


class JavaResource(JavaAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaResource0(JavaResource, AST):
    pass


class JavaResource1(JavaResource, AST):
    pass


class JavaResourceSpecification(JavaAST, AST):
    pass


class JavaReturn(JavaAST, TerminalSymbol, AST):
    pass


class JavaReturnStatement(JavaStatement, ReturnAST, AST):
    pass


class JavaReturnStatement0(JavaReturnStatement, AST):
    pass


class JavaReturnStatement1(JavaReturnStatement, AST):
    pass


class JavaScopedIdentifier(JavaAST, AST):
    @_property
    def scope(self) -> Optional[AST]:
        return self.child_slot("scope")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaScopedTypeIdentifier(JavaSimpleType, AST):
    pass


class JavaScopedTypeIdentifier0(JavaScopedTypeIdentifier, AST):
    pass


class JavaScopedTypeIdentifier1(JavaScopedTypeIdentifier, AST):
    pass


class JavaSealed(JavaAST, TerminalSymbol, AST):
    pass


class JavaShort(JavaAST, TerminalSymbol, AST):
    pass


class JavaSourceTextFragment(JavaAST, SourceTextFragment, AST):
    pass


class JavaSourceTextFragmentTree(ErrorTree, JavaAST, AST):
    pass


class JavaSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, JavaAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class JavaSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, JavaAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class JavaSpreadParameter(JavaAST, AST):
    pass


class JavaSpreadParameter0(JavaSpreadParameter, AST):
    pass


class JavaSpreadParameter1(JavaSpreadParameter, AST):
    pass


class JavaStatic(JavaAST, TerminalSymbol, AST):
    pass


class JavaStaticInitializer(JavaAST, AST):
    pass


class JavaStrictfp(JavaAST, TerminalSymbol, AST):
    pass


class JavaStringLiteral(JavaLiteral, StringAST, AST):
    pass


class JavaSuper(JavaAST, AST):
    pass


class JavaSuperInterfaces(JavaAST, AST):
    pass


class JavaSuperclass(JavaAST, AST):
    pass


class JavaSwitch(JavaAST, TerminalSymbol, AST):
    pass


class JavaSwitchBlock(JavaAST, AST):
    pass


class JavaSwitchBlockStatementGroup(JavaAST, AST):
    pass


class JavaSwitchExpression(JavaStatement, JavaExpression, ControlFlowAST, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavaSwitchLabel(JavaAST, AST):
    pass


class JavaSwitchLabel0(JavaSwitchLabel, AST):
    pass


class JavaSwitchLabel1(JavaSwitchLabel, AST):
    pass


class JavaSwitchRule(JavaAST, AST):
    pass


class JavaSynchronized(JavaAST, TerminalSymbol, AST):
    pass


class JavaSynchronizedStatement(JavaStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavaTernaryExpression(JavaExpression, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class JavaTextBlock(JavaLiteral, AST):
    pass


class JavaThis(JavaPrimaryExpression, AST):
    pass


class JavaThrow(JavaAST, TerminalSymbol, AST):
    pass


class JavaThrowStatement(JavaStatement, AST):
    pass


class JavaThrows(JavaAST, AST):
    pass


class JavaThrowsTerminal(JavaAST, TerminalSymbol, AST):
    pass


class JavaTo(JavaAST, TerminalSymbol, AST):
    pass


class JavaTransient(JavaAST, TerminalSymbol, AST):
    pass


class JavaTransitive(JavaAST, TerminalSymbol, AST):
    pass


class BooleanTrueAST(BooleanAST, AST):
    pass


class JavaTrue(JavaLiteral, BooleanTrueAST, AST):
    pass


class JavaTry(JavaAST, TerminalSymbol, AST):
    pass


class JavaTryStatement(JavaStatement, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavaTryStatement0(JavaTryStatement, AST):
    pass


class JavaTryStatement1(JavaTryStatement, AST):
    pass


class JavaTryWithResourcesStatement(JavaStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def resources(self) -> Optional[AST]:
        return self.child_slot("resources")  # type: ignore


class JavaTryWithResourcesStatement0(JavaTryWithResourcesStatement, AST):
    pass


class JavaTryWithResourcesStatement1(JavaTryWithResourcesStatement, AST):
    pass


class JavaTypeArguments(JavaAST, AST):
    pass


class JavaTypeArguments0(JavaTypeArguments, AST):
    pass


class JavaTypeArguments1(JavaTypeArguments, AST):
    pass


class JavaTypeBound(JavaAST, AST):
    pass


class JavaTypeIdentifier(JavaSimpleType, TypeIdentifierAST, AST):
    pass


class JavaTypeList(JavaAST, AST):
    pass


class JavaTypeParameter(JavaAST, AST):
    pass


class JavaTypeParameter0(JavaTypeParameter, AST):
    pass


class JavaTypeParameter1(JavaTypeParameter, AST):
    pass


class JavaTypeParameters(JavaAST, AST):
    pass


class JavaUnaryExpression(JavaExpression, UnaryAST, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def operand(self) -> Optional[AST]:
        return self.child_slot("operand")  # type: ignore


class JavaUpdateExpression(JavaExpression, AssignmentAST, AST):
    pass


class JavaUpdateExpression0(JavaUpdateExpression, AST):
    pass


class JavaUpdateExpression1(JavaUpdateExpression, AST):
    pass


class JavaUpdateExpression2(JavaUpdateExpression, AST):
    pass


class JavaUpdateExpression3(JavaUpdateExpression, AST):
    pass


class JavaUses(JavaAST, TerminalSymbol, AST):
    pass


class JavaUsesModuleDirective(JavaModuleDirective, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class JavaVariableDeclarator(VariableDeclarationAST, JavaAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def dimensions(self) -> Optional[AST]:
        return self.child_slot("dimensions")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavaVariableDeclarator0(JavaVariableDeclarator, AST):
    pass


class JavaVariableDeclarator1(JavaVariableDeclarator, AST):
    pass


class JavaVoidType(JavaSimpleType, AST):
    pass


class JavaVolatile(JavaAST, TerminalSymbol, AST):
    pass


class JavaWhile(JavaAST, TerminalSymbol, AST):
    pass


class JavaWhileStatement(JavaStatement, WhileAST, LoopAST, AST):
    pass


class JavaWildcard(JavaAST, AST):
    pass


class JavaWildcard0(JavaWildcard, AST):
    pass


class JavaWildcard1(JavaWildcard, AST):
    pass


class JavaWildcard2(JavaWildcard, AST):
    pass


class JavaWith(JavaAST, TerminalSymbol, AST):
    pass


class JavaYield(JavaAST, TerminalSymbol, AST):
    pass


class JavaYieldStatement(JavaStatement, AST):
    pass


class JavaOpenBracket(JavaAST, TerminalSymbol, AST):
    pass


class JavaCloseBracket(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseXor(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseXorAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaOpenBrace(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseOr(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseOrAssign(JavaAST, TerminalSymbol, AST):
    pass


class JavaLogicalOr(JavaAST, TerminalSymbol, AST):
    pass


class JavaCloseBrace(JavaAST, TerminalSymbol, AST):
    pass


class JavaBitwiseNot(JavaAST, TerminalSymbol, AST):
    pass


class ECMAAST(AST):
    pass


class JavascriptAST(ECMAAST, CLikeSyntaxAST, NormalScopeAST, AST):
    pass


class JavascriptLogicalNot(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptNotEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptStrictlyNotEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDoubleQuote(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptOpenTemplateLiteral(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptModulo(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptModuleAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseAnd(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLogicalAnd(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLogicalAndAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseAndAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptSingleQuote(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptOpenParenthesis(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptCloseParenthesis(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptMultiply(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptPow(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptPowAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptMultiplyAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAdd(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptIncrement(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAddAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptComma(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptSubtract(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDecrement(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptSubtractAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAutomaticSemicolon(JavascriptAST, AST):
    pass


class JavascriptTemplateChars(JavascriptAST, AST):
    pass


class JavascriptTernaryQmark(JavascriptAST, AST):
    pass


class JavascriptDot(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptEllipsis(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDivide(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDivideAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptColon(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptSemicolon(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLessThan(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitshiftLeft(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitshiftLeftAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLessThanOrEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptStrictlyEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptEqualArrow(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptGreaterThan(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptGreaterThanOrEqual(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitshiftRight(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitshiftRightAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptUnsignedBitshiftRight(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptUnsignedBitshiftRightAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptQuestion(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptChaining(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptNullishCoalescing(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptNullishCoalescingAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptMatrixMultiply(JavascriptAST, TerminalSymbol, AST):
    pass


class ECMAArguments(AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class JavascriptArguments(ECMAArguments, ArgumentsAST, JavascriptAST, AST):
    pass


class JavascriptArguments0(JavascriptArguments, AST):
    pass


class JavascriptArguments1(JavascriptArguments, AST):
    pass


class JavascriptArguments2(JavascriptArguments, AST):
    pass


class JavascriptExpression(JavascriptAST, AST):
    pass


class JavascriptPrimaryExpression(JavascriptExpression, AST):
    pass


class JavascriptArray(JavascriptPrimaryExpression, AST):
    pass


class JavascriptArray0(JavascriptArray, AST):
    pass


class JavascriptArray1(JavascriptArray, AST):
    pass


class JavascriptArray2(JavascriptArray, AST):
    pass


class JavascriptPattern(JavascriptAST, AST):
    pass


class JavascriptArrayPattern(JavascriptPattern, AST):
    pass


class JavascriptArrayPattern0(JavascriptArrayPattern, AST):
    pass


class JavascriptArrayPattern1(JavascriptArrayPattern, AST):
    pass


class JavascriptArrayPattern2(JavascriptArrayPattern, AST):
    pass


class JavascriptArrowFunction(JavascriptPrimaryExpression, LambdaAST, AST):
    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore


class JavascriptArrowFunction0(JavascriptArrowFunction, AST):
    pass


class JavascriptArrowFunction1(JavascriptArrowFunction, AST):
    pass


class JavascriptAs(JavascriptAST, TerminalSymbol, AST):
    pass


class ECMAAssignmentExpression(AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavascriptAssignmentExpression(JavascriptExpression, AssignmentAST, ECMAAssignmentExpression, AST):
    pass


class ECMAAssignmentPattern(AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavascriptAssignmentPattern(AssignmentAST, ECMAAssignmentPattern, JavascriptAST, AST):
    pass


class JavascriptAsync(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAugmentedAssignmentExpression(JavascriptExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavascriptAwait(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptAwaitExpression(JavascriptExpression, AST):
    pass


class JavascriptBinaryExpression(JavascriptExpression, BinaryAST, AST):
    pass


class JavascriptBlot(JavascriptAST, Blot, AST):
    pass


class JavascriptBreak(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptStatement(StatementAST, JavascriptAST, AST):
    pass


class JavascriptBreakStatement(JavascriptStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class ECMACallExpression(AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore


class JavascriptCallExpression(JavascriptPrimaryExpression, ECMACallExpression, CallAST, AST):
    pass


class JavascriptCallExpression0(JavascriptCallExpression, AST):
    pass


class JavascriptCallExpression1(JavascriptCallExpression, AST):
    pass


class JavascriptCase(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptCatch(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptCatchClause(CatchAST, JavascriptAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore


class JavascriptCatchClause0(JavascriptCatchClause, AST):
    pass


class JavascriptCatchClause1(JavascriptCatchClause, AST):
    pass


class JavascriptClass(JavascriptPrimaryExpression, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class JavascriptClass0(JavascriptClass, AST):
    pass


class JavascriptClass1(JavascriptClass, AST):
    pass


class JavascriptClassBody(JavascriptAST, AST):
    @_property
    def member(self) -> List[AST]:
        return self.child_slot("member")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptDeclaration(JavascriptStatement, AST):
    pass


class JavascriptClassDeclaration(JavascriptDeclaration, ClassAST, AST):
    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class JavascriptClassDeclaration0(JavascriptClassDeclaration, AST):
    pass


class JavascriptClassDeclaration1(JavascriptClassDeclaration, AST):
    pass


class JavascriptClassHeritage(JavascriptAST, AST):
    pass


class JavascriptClassTerminal(JavascriptPrimaryExpression, TerminalSymbol, AST):
    pass


class ECMAComment(CommentAST, AST):
    pass


class JavascriptComment(ECMAComment, CommentAST, JavascriptAST, AST):
    pass


class JavascriptComputedPropertyName(JavascriptAST, AST):
    pass


class JavascriptConst(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptContinue(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptContinueStatement(JavascriptStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptDebugger(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDebuggerStatement(JavascriptStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptDecorator(JavascriptAST, AST):
    pass


class JavascriptDecorator0(JavascriptDecorator, AST):
    pass


class JavascriptDecorator1(JavascriptDecorator, AST):
    pass


class JavascriptDecorator2(JavascriptDecorator, AST):
    pass


class JavascriptDefault(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDelete(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDo(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptDoStatement(JavascriptStatement, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptElse(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptElseClause(JavascriptAST, AST):
    pass


class JavascriptEmptyStatement(JavascriptStatement, AST):
    pass


class ECMAError(AST):
    pass


class JavascriptError(JavascriptAST, ECMAError, ParseErrorAST, AST):
    pass


class JavascriptErrorTree(ErrorTree, JavascriptAST, AST):
    pass


class JavascriptErrorVariationPoint(ErrorVariationPoint, JavascriptAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class JavascriptErrorVariationPointTree(ErrorVariationPoint, JavascriptAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class JavascriptEscapeSequence(JavascriptAST, AST):
    pass


class JavascriptExport(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptExportClause(JavascriptAST, AST):
    pass


class JavascriptExportClause0(JavascriptExportClause, AST):
    pass


class JavascriptExportClause1(JavascriptExportClause, AST):
    pass


class JavascriptExportClause2(JavascriptExportClause, AST):
    pass


class JavascriptExportClause3(JavascriptExportClause, AST):
    pass


class JavascriptExportSpecifier(JavascriptAST, AST):
    pass


class JavascriptExportStatement(JavascriptStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore

    @_property
    def default(self) -> Optional[AST]:
        return self.child_slot("default")  # type: ignore

    @_property
    def declaration(self) -> Optional[AST]:
        return self.child_slot("declaration")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore


class JavascriptExportStatement0(JavascriptExportStatement, AST):
    pass


class JavascriptExportStatement1(JavascriptExportStatement, AST):
    pass


class JavascriptExpressionStatement(JavascriptStatement, ExpressionStatementAST, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptExtends(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptFalse(JavascriptPrimaryExpression, BooleanFalseAST, AST):
    pass


class JavascriptFieldDefinition(JavascriptAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def property(self) -> Optional[AST]:
        return self.child_slot("property")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class JavascriptFieldDefinition0(JavascriptFieldDefinition, AST):
    pass


class JavascriptFieldDefinition1(JavascriptFieldDefinition, AST):
    pass


class JavascriptFinally(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptFinallyClause(JavascriptAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptFor(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptForInStatement(JavascriptStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore


class JavascriptForInStatement0(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement1(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement2(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement3(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement4(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement5(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement6(JavascriptForInStatement, AST):
    pass


class JavascriptForInStatement7(JavascriptForInStatement, AST):
    pass


class JavascriptForStatement(JavascriptStatement, LoopAST, AST):
    @_property
    def initializer(self) -> Optional[AST]:
        return self.child_slot("initializer")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def increment(self) -> Optional[AST]:
        return self.child_slot("increment")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptFormalParameters(ParametersAST, JavascriptAST, AST):
    pass


class JavascriptFormalParameters0(JavascriptFormalParameters, AST):
    pass


class JavascriptFormalParameters1(JavascriptFormalParameters, AST):
    pass


class JavascriptFrom(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptFunction(JavascriptPrimaryExpression, LambdaAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavascriptFunctionDeclaration(JavascriptDeclaration, FunctionDeclarationAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def javascript_async(self) -> Optional[AST]:
        return self.child_slot("javascript_async")  # type: ignore


class JavascriptFunctionTerminal(JavascriptPrimaryExpression, LambdaAST, TerminalSymbol, AST):
    pass


class JavascriptGeneratorFunction(JavascriptPrimaryExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptGeneratorFunctionDeclaration(JavascriptDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptGet(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptHashBangLine(JavascriptAST, AST):
    pass


class JavascriptIdentifier(JavascriptPattern, JavascriptPrimaryExpression, IdentifierAST, AST):
    pass


class JavascriptIf(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptIfStatement(JavascriptStatement, IfAST, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class JavascriptIfStatement0(JavascriptIfStatement, AST):
    pass


class JavascriptIfStatement1(JavascriptIfStatement, AST):
    pass


class JavascriptImport(JavascriptPrimaryExpression, AST):
    pass


class JavascriptImportClause(JavascriptAST, AST):
    pass


class JavascriptImportClause0(JavascriptImportClause, AST):
    pass


class JavascriptImportClause1(JavascriptImportClause, AST):
    pass


class JavascriptImportClause2(JavascriptImportClause, AST):
    pass


class JavascriptImportSpecifier(JavascriptAST, AST):
    pass


class JavascriptImportStatement(JavascriptStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore

    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore


class JavascriptImportStatement0(JavascriptImportStatement, AST):
    pass


class JavascriptImportStatement1(JavascriptImportStatement, AST):
    pass


class JavascriptImportTerminal(JavascriptPrimaryExpression, TerminalSymbol, AST):
    pass


class JavascriptIn(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptInnerWhitespace(JavascriptAST, InnerWhitespace, AST):
    pass


class JavascriptInstanceof(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptJsxAttribute(JavascriptAST, AST):
    pass


class JavascriptJsxAttribute0(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxAttribute1(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxAttribute2(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxAttribute3(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxAttribute4(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxAttribute5(JavascriptJsxAttribute, AST):
    pass


class JavascriptJsxClosingElement(JavascriptAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavascriptJsxElement(JavascriptExpression, AST):
    @_property
    def open_tag(self) -> Optional[AST]:
        return self.child_slot("open_tag")  # type: ignore

    @_property
    def close_tag(self) -> Optional[AST]:
        return self.child_slot("close_tag")  # type: ignore


class JavascriptJsxExpression(JavascriptAST, AST):
    pass


class JavascriptJsxExpression0(JavascriptJsxExpression, AST):
    pass


class JavascriptJsxExpression1(JavascriptJsxExpression, AST):
    pass


class JavascriptJsxFragment(JavascriptExpression, AST):
    pass


class JavascriptJsxNamespaceName(JavascriptAST, AST):
    pass


class JavascriptJsxOpeningElement(JavascriptAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore


class JavascriptJsxSelfClosingElement(JavascriptExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore


class JavascriptJsxText(JavascriptAST, AST):
    pass


class JavascriptLabeledStatement(JavascriptStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptLet(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLexicalDeclaration(JavascriptDeclaration, AST):
    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class ECMAMemberExpression(AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def property(self) -> Optional[AST]:
        return self.child_slot("property")  # type: ignore


class JavascriptMemberExpression(JavascriptPattern, JavascriptPrimaryExpression, ECMAMemberExpression, FieldAST, AST):
    pass


class JavascriptMemberExpression0(JavascriptMemberExpression, AST):
    pass


class JavascriptMemberExpression1(JavascriptMemberExpression, AST):
    pass


class JavascriptMetaProperty(JavascriptPrimaryExpression, AST):
    pass


class JavascriptMethodDefinition(JavascriptAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class JavascriptMethodDefinition0(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition1(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition2(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition3(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition4(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition5(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition6(JavascriptMethodDefinition, AST):
    pass


class JavascriptMethodDefinition7(JavascriptMethodDefinition, AST):
    pass


class JavascriptNamedImports(JavascriptAST, AST):
    pass


class JavascriptNamedImports0(JavascriptNamedImports, AST):
    pass


class JavascriptNamedImports1(JavascriptNamedImports, AST):
    pass


class JavascriptNamedImports2(JavascriptNamedImports, AST):
    pass


class JavascriptNamedImports3(JavascriptNamedImports, AST):
    pass


class JavascriptNamespaceExport(JavascriptAST, AST):
    pass


class JavascriptNamespaceImport(JavascriptAST, AST):
    pass


class JavascriptNestedIdentifier(JavascriptAST, AST):
    pass


class JavascriptNew(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptNewExpression(JavascriptExpression, AST):
    @_property
    def constructor(self) -> Optional[AST]:
        return self.child_slot("constructor")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class JavascriptNull(JavascriptPrimaryExpression, AST):
    pass


class FloatAST(NumberAST, AST):
    pass


class JavascriptNumber(JavascriptPrimaryExpression, FloatAST, AST):
    pass


class JavascriptObject(JavascriptPrimaryExpression, AST):
    pass


class JavascriptObject0(JavascriptObject, AST):
    pass


class JavascriptObject1(JavascriptObject, AST):
    pass


class JavascriptObject2(JavascriptObject, AST):
    pass


class JavascriptObject3(JavascriptObject, AST):
    pass


class JavascriptObjectAssignmentPattern(JavascriptAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavascriptObjectPattern(JavascriptPattern, AST):
    pass


class JavascriptObjectPattern0(JavascriptObjectPattern, AST):
    pass


class JavascriptObjectPattern1(JavascriptObjectPattern, AST):
    pass


class JavascriptObjectPattern2(JavascriptObjectPattern, AST):
    pass


class JavascriptObjectPattern3(JavascriptObjectPattern, AST):
    pass


class JavascriptOf(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptPair(JavascriptAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class JavascriptPairPattern(JavascriptAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class JavascriptParenthesizedExpression(JavascriptPrimaryExpression, ParenthesizedExpressionAST, AST):
    pass


class JavascriptPrivatePropertyIdentifier(JavascriptAST, AST):
    pass


class JavascriptProgram(RootAST, JavascriptAST, AST):
    pass


class JavascriptProgram0(JavascriptProgram, AST):
    pass


class JavascriptProgram1(JavascriptProgram, AST):
    pass


class JavascriptPropertyIdentifier(IdentifierAST, JavascriptAST, AST):
    pass


class JavascriptRegex(JavascriptPrimaryExpression, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def flags(self) -> Optional[AST]:
        return self.child_slot("flags")  # type: ignore


class JavascriptRegexFlags(JavascriptAST, AST):
    pass


class JavascriptRegexPattern(JavascriptAST, AST):
    pass


class ECMARestPattern(AST):
    pass


class JavascriptRestPattern(JavascriptPattern, ECMARestPattern, AST):
    pass


class JavascriptRestPattern0(JavascriptRestPattern, AST):
    pass


class JavascriptRestPattern1(JavascriptRestPattern, AST):
    pass


class JavascriptRestPattern2(JavascriptRestPattern, AST):
    pass


class JavascriptReturn(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptReturnStatement(JavascriptStatement, ReturnAST, AST):
    pass


class JavascriptReturnStatement0(JavascriptReturnStatement, AST):
    pass


class JavascriptReturnStatement1(JavascriptReturnStatement, AST):
    pass


class JavascriptSequenceExpression(JavascriptAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class JavascriptSet(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptShorthandPropertyIdentifier(IdentifierAST, JavascriptAST, AST):
    pass


class JavascriptShorthandPropertyIdentifierPattern(IdentifierAST, JavascriptAST, AST):
    pass


class JavascriptSourceTextFragment(JavascriptAST, SourceTextFragment, AST):
    pass


class JavascriptSourceTextFragmentTree(ErrorTree, JavascriptAST, AST):
    pass


class JavascriptSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, JavascriptAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class JavascriptSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, JavascriptAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class JavascriptSpreadElement(JavascriptAST, AST):
    pass


class JavascriptStatementBlock(JavascriptStatement, CompoundAST, AST):
    pass


class JavascriptStatementIdentifier(JavascriptAST, AST):
    pass


class JavascriptStatic(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptString(JavascriptPrimaryExpression, StringAST, AST):
    pass


class JavascriptString0(JavascriptString, AST):
    pass


class JavascriptString1(JavascriptString, AST):
    pass


class JavascriptStringFragment(JavascriptAST, AST):
    pass


class JavascriptSubscriptExpression(JavascriptPattern, JavascriptPrimaryExpression, SubscriptAST, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def index(self) -> Optional[AST]:
        return self.child_slot("index")  # type: ignore


class JavascriptSuper(JavascriptPrimaryExpression, AST):
    pass


class JavascriptSwitch(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptSwitchBody(JavascriptAST, AST):
    pass


class JavascriptSwitchCase(JavascriptAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptSwitchDefault(JavascriptAST, AST):
    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptSwitchStatement(JavascriptStatement, ControlFlowAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptTarget(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptTemplateString(JavascriptPrimaryExpression, AST):
    pass


class JavascriptTemplateSubstitution(JavascriptAST, AST):
    pass


class JavascriptTernaryExpression(JavascriptExpression, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class JavascriptThis(JavascriptPrimaryExpression, AST):
    pass


class JavascriptThrow(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptThrowStatement(JavascriptStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class JavascriptTrue(JavascriptPrimaryExpression, BooleanTrueAST, AST):
    pass


class JavascriptTry(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptTryStatement(JavascriptStatement, ControlFlowAST, AST):
    @_property
    def finalizer(self) -> Optional[AST]:
        return self.child_slot("finalizer")  # type: ignore

    @_property
    def handler(self) -> Optional[AST]:
        return self.child_slot("handler")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptTryStatement0(JavascriptTryStatement, AST):
    pass


class JavascriptTryStatement1(JavascriptTryStatement, AST):
    pass


class JavascriptTryStatement2(JavascriptTryStatement, AST):
    pass


class JavascriptTryStatement3(JavascriptTryStatement, AST):
    pass


class JavascriptTypeof(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptUnaryExpression(JavascriptExpression, UnaryAST, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class JavascriptUndefined(JavascriptPattern, JavascriptPrimaryExpression, AST):
    pass


class JavascriptUpdateExpression(JavascriptExpression, AssignmentAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class JavascriptUpdateExpression0(JavascriptUpdateExpression, AST):
    pass


class JavascriptUpdateExpression1(JavascriptUpdateExpression, AST):
    pass


class JavascriptVar(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptVariableDeclaration(JavascriptDeclaration, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class ECMAVariableDeclarator(AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class JavascriptVariableDeclarator(ECMAVariableDeclarator, JavascriptAST, AST):
    pass


class JavascriptVariableDeclarator0(JavascriptVariableDeclarator, AST):
    pass


class JavascriptVariableDeclarator1(JavascriptVariableDeclarator, AST):
    pass


class JavascriptVoid(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptWhile(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptWhileStatement(JavascriptStatement, LoopAST, WhileAST, AST):
    pass


class JavascriptWith(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptWithStatement(JavascriptStatement, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class JavascriptYield(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptYieldExpression(JavascriptExpression, AST):
    pass


class JavascriptYieldExpression0(JavascriptYieldExpression, AST):
    pass


class JavascriptYieldExpression1(JavascriptYieldExpression, AST):
    pass


class JavascriptYieldExpression2(JavascriptYieldExpression, AST):
    pass


class JavascriptOpenBracket(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptCloseBracket(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseXor(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseXorAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBackQuote(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptOpenBrace(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseOr(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseOrAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLogicalOr(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptLogicalOrAssign(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptCloseBrace(JavascriptAST, TerminalSymbol, AST):
    pass


class JavascriptBitwiseNot(JavascriptAST, TerminalSymbol, AST):
    pass


class PythonAST(AST):
    pass


class PythonNotEqual(PythonAST, TerminalSymbol, AST):
    pass


class PythonDoubleQuote(PythonAST, TerminalSymbol, AST):
    pass


class PythonModulo(PythonAST, TerminalSymbol, AST):
    pass


class PythonModuleAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseAnd(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseAndAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonOpenParenthesis(PythonAST, TerminalSymbol, AST):
    pass


class PythonCloseParenthesis(PythonAST, TerminalSymbol, AST):
    pass


class PythonMultiply(PythonAST, TerminalSymbol, AST):
    pass


class PythonPow(PythonAST, TerminalSymbol, AST):
    pass


class PythonPowAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonMultiplyAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonAdd(PythonAST, TerminalSymbol, AST):
    pass


class PythonAddAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonComma(PythonAST, TerminalSymbol, AST):
    pass


class PythonSubtract(PythonAST, TerminalSymbol, AST):
    pass


class PythonFutureSubtract(PythonAST, TerminalSymbol, AST):
    pass


class PythonSubtractAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonDashArrow(PythonAST, TerminalSymbol, AST):
    pass


class PythonCompoundStatement(StatementAST, PythonAST, AST):
    pass


class PythonDedent(PythonAST, AST):
    pass


class PythonIndent(PythonAST, AST):
    pass


class PythonNewline(PythonAST, AST):
    pass


class PythonSimpleStatement(StatementAST, PythonAST, AST):
    pass


class PythonStringContent(PythonAST, AST):
    pass


class PythonStringEnd(PythonAST, AST):
    pass


class PythonStringStart(PythonAST, AST):
    pass


class PythonDot(PythonAST, TerminalSymbol, AST):
    pass


class PythonDivide(PythonAST, TerminalSymbol, AST):
    pass


class PythonFloorDivide(PythonAST, TerminalSymbol, AST):
    pass


class PythonFloorDivideAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonDivideAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonColon(PythonAST, TerminalSymbol, AST):
    pass


class PythonWalrus(PythonAST, TerminalSymbol, AST):
    pass


class PythonSemicolon(PythonAST, TerminalSymbol, AST):
    pass


class PythonLessThan(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitshiftLeft(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitshiftLeftAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonLessThanOrEqual(PythonAST, TerminalSymbol, AST):
    pass


class PythonNotEqualFlufl(PythonAST, TerminalSymbol, AST):
    pass


class PythonAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonEqual(PythonAST, TerminalSymbol, AST):
    pass


class PythonGreaterThan(PythonAST, TerminalSymbol, AST):
    pass


class PythonGreaterThanOrEqual(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitshiftRight(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitshiftRightAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonMatrixMultiply(PythonAST, TerminalSymbol, AST):
    pass


class PythonMatrixMultiplyAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonAliasedImport(PythonAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore


class PythonAnd(PythonAST, TerminalSymbol, AST):
    pass


class PythonArgumentList(ArgumentsAST, PythonAST, AST):
    pass


class PythonArgumentList0(PythonArgumentList, AST):
    pass


class PythonArgumentList1(PythonArgumentList, AST):
    pass


class PythonArgumentList2(PythonArgumentList, AST):
    pass


class PythonArgumentList3(PythonArgumentList, AST):
    pass


class PythonArgumentList4(PythonArgumentList, AST):
    pass


class PythonAs(PythonAST, TerminalSymbol, AST):
    pass


class PythonAssert(PythonAST, TerminalSymbol, AST):
    pass


class PythonAssertStatement(PythonSimpleStatement, AST):
    pass


class PythonAssignment(AssignmentAST, VariableDeclarationAST, PythonAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class PythonAssignment0(PythonAssignment, AST):
    pass


class PythonAssignment1(PythonAssignment, AST):
    pass


class PythonAssignment2(PythonAssignment, AST):
    pass


class PythonAsync(PythonAST, TerminalSymbol, AST):
    pass


class PythonExpression(ExpressionAST, PythonAST, AST):
    pass


class PythonPrimaryExpression(PythonExpression, AST):
    pass


class PythonPattern(PythonAST, AST):
    pass


class PythonAttribute(PythonPattern, PythonPrimaryExpression, FieldAST, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def attribute(self) -> Optional[AST]:
        return self.child_slot("attribute")  # type: ignore


class PythonAugmentedAssignment(AssignmentAST, PythonAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class PythonAwait(PythonExpression, AST):
    pass


class PythonAwaitTerminal(PythonExpression, TerminalSymbol, AST):
    pass


class PythonBinaryOperator(PythonPrimaryExpression, BinaryAST, AST):
    pass


class PythonBlock(CompoundAST, PythonAST, AST):
    pass


class PythonBlock0(PythonBlock, AST):
    pass


class PythonBlock1(PythonBlock, AST):
    pass


class PythonBlock2(PythonBlock, AST):
    pass


class PythonBlot(PythonAST, Blot, AST):
    pass


class PythonBooleanOperator(PythonExpression, BinaryAST, AST):
    pass


class PythonBreak(PythonAST, TerminalSymbol, AST):
    pass


class PythonBreakStatement(PythonSimpleStatement, AST):
    pass


class PythonCall(PythonPrimaryExpression, CallAST, AST):
    pass


class PythonChevron(PythonAST, AST):
    pass


class PythonClass(PythonAST, TerminalSymbol, AST):
    pass


class PythonClassDefinition(PythonCompoundStatement, ClassAST, AST):
    @_property
    def superclasses(self) -> Optional[AST]:
        return self.child_slot("superclasses")  # type: ignore


class PythonClassDefinition0(PythonClassDefinition, AST):
    pass


class PythonClassDefinition1(PythonClassDefinition, AST):
    pass


class PythonComment(CommentAST, PythonAST, AST):
    pass


class PythonComparisonOperator(PythonExpression, AST):
    @_property
    def operators(self) -> List[AST]:
        return self.child_slot("operators")  # type: ignore


class PythonComparisonOperator0(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator1(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator10(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator2(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator3(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator4(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator5(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator6(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator7(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator8(PythonComparisonOperator, AST):
    pass


class PythonComparisonOperator9(PythonComparisonOperator, AST):
    pass


class PythonConcatenatedString(PythonPrimaryExpression, AST):
    pass


class PythonConditionalExpression(PythonExpression, ControlFlowAST, AST):
    pass


class PythonContinue(PythonAST, TerminalSymbol, AST):
    pass


class PythonContinueStatement(PythonSimpleStatement, AST):
    pass


class PythonDecoratedDefinition(PythonCompoundStatement, AST):
    @_property
    def definition(self) -> Optional[AST]:
        return self.child_slot("definition")  # type: ignore


class PythonDecorator(PythonAST, AST):
    pass


class PythonDef(PythonAST, TerminalSymbol, AST):
    pass


class PythonParameter(ParameterAST, PythonAST, AST):
    pass


class PythonDefaultParameter(PythonParameter, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonDel(PythonAST, TerminalSymbol, AST):
    pass


class PythonDeleteStatement(PythonSimpleStatement, AST):
    pass


class PythonDictionary(PythonPrimaryExpression, AST):
    pass


class PythonDictionary0(PythonDictionary, AST):
    pass


class PythonDictionary1(PythonDictionary, AST):
    pass


class PythonDictionary2(PythonDictionary, AST):
    pass


class PythonDictionary3(PythonDictionary, AST):
    pass


class PythonDictionaryComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonDictionarySplat(PythonAST, AST):
    pass


class PythonDictionarySplatPattern(PythonParameter, AST):
    pass


class PythonDictionarySplatPattern0(PythonDictionarySplatPattern, AST):
    pass


class PythonDictionarySplatPattern1(PythonDictionarySplatPattern, AST):
    pass


class PythonDottedName(PythonAST, AST):
    pass


class PythonElif(PythonAST, TerminalSymbol, AST):
    pass


class PythonElifClause(PythonAST, AST):
    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class PythonElifClause0(PythonElifClause, AST):
    pass


class PythonElifClause1(PythonElifClause, AST):
    pass


class PythonEllipsis(PythonPrimaryExpression, AST):
    pass


class PythonElse(PythonAST, TerminalSymbol, AST):
    pass


class PythonElseClause(PythonAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonElseClause0(PythonElseClause, AST):
    pass


class PythonElseClause1(PythonElseClause, AST):
    pass


class PythonEmptyArgumentList(PythonArgumentList, AST):
    pass


class PythonParameters(ParametersAST, PythonAST, AST):
    pass


class PythonEmptyParameters(PythonParameters, AST):
    pass


class PythonTuple(PythonPrimaryExpression, AST):
    pass


class PythonEmptyTuple(PythonTuple, AST):
    pass


class PythonError(PythonAST, ParseErrorAST, AST):
    pass


class PythonErrorTree(ErrorTree, PythonAST, AST):
    pass


class PythonErrorVariationPoint(ErrorVariationPoint, PythonAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class PythonErrorVariationPointTree(ErrorVariationPoint, PythonAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class PythonEscapeSequence(PythonAST, AST):
    pass


class PythonExcept(PythonAST, TerminalSymbol, AST):
    pass


class PythonExceptClause(CatchAST, PythonAST, AST):
    pass


class PythonExceptClause0(PythonExceptClause, AST):
    pass


class PythonExceptClause1(PythonExceptClause, AST):
    pass


class PythonExceptClause2(PythonExceptClause, AST):
    pass


class PythonExceptClause3(PythonExceptClause, AST):
    pass


class PythonExceptClause4(PythonExceptClause, AST):
    pass


class PythonExceptClause5(PythonExceptClause, AST):
    pass


class PythonExec(PythonAST, TerminalSymbol, AST):
    pass


class PythonExecStatement(PythonSimpleStatement, AST):
    @_property
    def code(self) -> Optional[AST]:
        return self.child_slot("code")  # type: ignore


class PythonExecStatement0(PythonExecStatement, AST):
    pass


class PythonExecStatement1(PythonExecStatement, AST):
    pass


class PythonExpressionList(PythonAST, AST):
    pass


class PythonExpressionList0(PythonExpressionList, AST):
    pass


class PythonExpressionList1(PythonExpressionList, AST):
    pass


class PythonExpressionStatement(PythonSimpleStatement, ExpressionStatementAST, AST):
    pass


class PythonExpressionStatement0(PythonExpressionStatement, AST):
    pass


class PythonExpressionStatement1(PythonExpressionStatement, AST):
    pass


class PythonFalse(PythonPrimaryExpression, BooleanFalseAST, AST):
    pass


class PythonFinally(PythonAST, TerminalSymbol, AST):
    pass


class PythonFinallyClause(PythonAST, AST):
    pass


class PythonFinallyClause0(PythonFinallyClause, AST):
    pass


class PythonFinallyClause1(PythonFinallyClause, AST):
    pass


class PythonFloat(PythonPrimaryExpression, FloatAST, AST):
    pass


class PythonFor(PythonAST, TerminalSymbol, AST):
    pass


class PythonForInClause(LoopAST, PythonAST, AST):
    @_property
    def right(self) -> List[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore


class PythonForInClause0(PythonForInClause, AST):
    pass


class PythonForInClause1(PythonForInClause, AST):
    pass


class PythonForStatement(PythonCompoundStatement, LoopAST, AST):
    @_property
    def python_async(self) -> Optional[AST]:
        return self.child_slot("python_async")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore


class PythonForStatement0(PythonForStatement, AST):
    pass


class PythonForStatement1(PythonForStatement, AST):
    pass


class PythonFormatExpression(PythonAST, AST):
    pass


class PythonFormatSpecifier(PythonAST, AST):
    pass


class PythonFrom(PythonAST, TerminalSymbol, AST):
    pass


class PythonFunctionDefinition(PythonCompoundStatement, FunctionDeclarationAST, AST):
    @_property
    def python_async(self) -> Optional[AST]:
        return self.child_slot("python_async")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class PythonFunctionDefinition0(PythonFunctionDefinition, AST):
    pass


class PythonFunctionDefinition1(PythonFunctionDefinition, AST):
    pass


class PythonFunctionDefinition2(PythonFunctionDefinition, AST):
    pass


class PythonFunctionDefinition3(PythonFunctionDefinition, AST):
    pass


class PythonFutureImportStatement(PythonSimpleStatement, AST):
    @_property
    def name(self) -> List[AST]:
        return self.child_slot("name")  # type: ignore


class PythonFutureImportStatement0(PythonFutureImportStatement, AST):
    pass


class PythonFutureImportStatement1(PythonFutureImportStatement, AST):
    pass


class PythonGeneratorExpression(PythonPrimaryExpression, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonGlobal(PythonAST, TerminalSymbol, AST):
    pass


class PythonGlobalStatement(PythonSimpleStatement, AST):
    pass


class PythonIdentifier(PythonParameter, PythonPattern, PythonPrimaryExpression, IdentifierAST, AST):
    pass


class PythonIf(PythonAST, TerminalSymbol, AST):
    pass


class PythonIfClause(PythonAST, AST):
    pass


class PythonIfStatement(PythonCompoundStatement, IfAST, AST):
    @_property
    def alternative(self) -> List[AST]:
        return self.child_slot("alternative")  # type: ignore


class PythonIfStatement0(PythonIfStatement, AST):
    pass


class PythonIfStatement1(PythonIfStatement, AST):
    pass


class PythonIfStatement2(PythonIfStatement, AST):
    pass


class PythonIfStatement3(PythonIfStatement, AST):
    pass


class PythonImport(PythonAST, TerminalSymbol, AST):
    pass


class PythonImportFromStatement(PythonSimpleStatement, AST):
    @_property
    def module_name(self) -> Optional[AST]:
        return self.child_slot("module_name")  # type: ignore

    @_property
    def name(self) -> List[AST]:
        return self.child_slot("name")  # type: ignore


class PythonImportFromStatement0(PythonImportFromStatement, AST):
    pass


class PythonImportFromStatement1(PythonImportFromStatement, AST):
    pass


class PythonImportFromStatement2(PythonImportFromStatement, AST):
    pass


class PythonImportPrefix(PythonAST, AST):
    pass


class PythonImportStatement(PythonSimpleStatement, AST):
    @_property
    def name(self) -> List[AST]:
        return self.child_slot("name")  # type: ignore


class PythonIn(PythonAST, TerminalSymbol, AST):
    pass


class PythonInnerWhitespace(PythonAST, InnerWhitespace, AST):
    pass


class IntegerAST(NumberAST, AST):
    pass


class PythonInteger(PythonPrimaryExpression, IntegerAST, AST):
    pass


class PythonInterpolation(PythonAST, AST):
    pass


class PythonInterpolation0(PythonInterpolation, AST):
    pass


class PythonInterpolation1(PythonInterpolation, AST):
    pass


class PythonInterpolation2(PythonInterpolation, AST):
    pass


class PythonInterpolation3(PythonInterpolation, AST):
    pass


class PythonIs(PythonAST, TerminalSymbol, AST):
    pass


class PythonKeywordArgument(VariableDeclarationAST, PythonAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonKeywordOnlySeparator(PythonParameter, AST):
    pass


class PythonLambda(PythonExpression, LambdaAST, AST):
    pass


class PythonLambdaParameters(ParametersAST, PythonAST, AST):
    pass


class PythonLambdaTerminal(PythonExpression, LambdaAST, TerminalSymbol, AST):
    pass


class PythonList(PythonPrimaryExpression, AST):
    pass


class PythonList0(PythonList, AST):
    pass


class PythonList1(PythonList, AST):
    pass


class PythonListComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonListPattern(PythonPattern, AST):
    pass


class PythonListPattern0(PythonListPattern, AST):
    pass


class PythonListPattern1(PythonListPattern, AST):
    pass


class PythonListSplat(PythonAST, AST):
    pass


class PythonListSplatPattern(PythonParameter, PythonPattern, AST):
    pass


class PythonListSplatPattern0(PythonListSplatPattern, AST):
    pass


class PythonListSplatPattern1(PythonListSplatPattern, AST):
    pass


class PythonModule(RootAST, PythonAST, AST):
    pass


class PythonNamedExpression(PythonExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonNone(PythonPrimaryExpression, AST):
    pass


class PythonNonlocal(PythonAST, TerminalSymbol, AST):
    pass


class PythonNonlocalStatement(PythonSimpleStatement, AST):
    pass


class PythonNot(PythonAST, TerminalSymbol, AST):
    pass


class PythonNotOperator(PythonExpression, UnaryAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class PythonOr(PythonAST, TerminalSymbol, AST):
    pass


class PythonPair(PythonAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonParameters0(PythonParameters, AST):
    pass


class PythonParenthesizedExpression(PythonPrimaryExpression, ParenthesizedExpressionAST, AST):
    pass


class PythonParenthesizedExpression0(PythonParenthesizedExpression, AST):
    pass


class PythonParenthesizedExpression1(PythonParenthesizedExpression, AST):
    pass


class PythonParenthesizedListSplat(PythonAST, AST):
    pass


class PythonParenthesizedListSplat0(PythonParenthesizedListSplat, AST):
    pass


class PythonParenthesizedListSplat1(PythonParenthesizedListSplat, AST):
    pass


class PythonPass(PythonAST, TerminalSymbol, AST):
    pass


class PythonPassStatement(PythonSimpleStatement, AST):
    pass


class PythonPatternList(PythonAST, AST):
    pass


class PythonPatternList0(PythonPatternList, AST):
    pass


class PythonPatternList1(PythonPatternList, AST):
    pass


class PythonPositionalOnlySeparator(PythonParameter, AST):
    pass


class PythonPrint(PythonAST, TerminalSymbol, AST):
    pass


class PythonPrintStatement(PythonSimpleStatement, AST):
    @_property
    def argument(self) -> List[AST]:
        return self.child_slot("argument")  # type: ignore


class PythonPrintStatement0(PythonPrintStatement, AST):
    pass


class PythonPrintStatement1(PythonPrintStatement, AST):
    pass


class PythonRaise(PythonAST, TerminalSymbol, AST):
    pass


class PythonRaiseStatement(PythonSimpleStatement, AST):
    @_property
    def cause(self) -> Optional[AST]:
        return self.child_slot("cause")  # type: ignore


class PythonRaiseStatement0(PythonRaiseStatement, AST):
    pass


class PythonRaiseStatement1(PythonRaiseStatement, AST):
    pass


class PythonRaiseStatement2(PythonRaiseStatement, AST):
    pass


class PythonRaiseStatement3(PythonRaiseStatement, AST):
    pass


class PythonRelativeImport(PythonAST, AST):
    pass


class PythonRelativeImport0(PythonRelativeImport, AST):
    pass


class PythonRelativeImport1(PythonRelativeImport, AST):
    pass


class PythonReturn(PythonAST, TerminalSymbol, AST):
    pass


class PythonReturnStatement(PythonSimpleStatement, ReturnAST, AST):
    pass


class PythonReturnStatement0(PythonReturnStatement, AST):
    pass


class PythonReturnStatement1(PythonReturnStatement, AST):
    pass


class PythonSet(PythonPrimaryExpression, AST):
    pass


class PythonSetComprehension(PythonPrimaryExpression, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonSlice(PythonAST, AST):
    pass


class PythonSlice0(PythonSlice, AST):
    pass


class PythonSlice1(PythonSlice, AST):
    pass


class PythonSlice10(PythonSlice, AST):
    pass


class PythonSlice11(PythonSlice, AST):
    pass


class PythonSlice2(PythonSlice, AST):
    pass


class PythonSlice3(PythonSlice, AST):
    pass


class PythonSlice4(PythonSlice, AST):
    pass


class PythonSlice5(PythonSlice, AST):
    pass


class PythonSlice6(PythonSlice, AST):
    pass


class PythonSlice7(PythonSlice, AST):
    pass


class PythonSlice8(PythonSlice, AST):
    pass


class PythonSlice9(PythonSlice, AST):
    pass


class PythonSourceTextFragment(PythonAST, SourceTextFragment, AST):
    pass


class PythonSourceTextFragmentTree(ErrorTree, PythonAST, AST):
    pass


class PythonSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, PythonAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class PythonSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, PythonAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class PythonString(PythonPrimaryExpression, StringAST, AST):
    pass


class PythonSubscript(PythonPattern, PythonPrimaryExpression, SubscriptAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def subscript(self) -> List[AST]:
        return self.child_slot("subscript")  # type: ignore


class PythonTrue(PythonPrimaryExpression, BooleanTrueAST, AST):
    pass


class PythonTry(PythonAST, TerminalSymbol, AST):
    pass


class PythonTryStatement(PythonCompoundStatement, ControlFlowAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonTryStatement0(PythonTryStatement, AST):
    pass


class PythonTryStatement1(PythonTryStatement, AST):
    pass


class PythonTryStatement2(PythonTryStatement, AST):
    pass


class PythonTryStatement3(PythonTryStatement, AST):
    pass


class PythonTryStatement4(PythonTryStatement, AST):
    pass


class PythonTryStatement5(PythonTryStatement, AST):
    pass


class PythonTryStatement6(PythonTryStatement, AST):
    pass


class PythonTryStatement7(PythonTryStatement, AST):
    pass


class PythonTryStatement8(PythonTryStatement, AST):
    pass


class PythonTryStatement9(PythonTryStatement, AST):
    pass


class PythonTuple0(PythonTuple, AST):
    pass


class PythonTuple1(PythonTuple, AST):
    pass


class PythonTuplePattern(PythonParameter, PythonPattern, AST):
    pass


class PythonTuplePattern0(PythonTuplePattern, AST):
    pass


class PythonTuplePattern1(PythonTuplePattern, AST):
    pass


class PythonTuplePattern2(PythonTuplePattern, AST):
    pass


class PythonType(PythonAST, AST):
    pass


class PythonTypeConversion(PythonAST, AST):
    pass


class PythonTypedDefaultParameter(PythonParameter, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonTypedParameter(PythonParameter, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class PythonUnaryOperator(PythonPrimaryExpression, UnaryAST, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class PythonWhile(PythonAST, TerminalSymbol, AST):
    pass


class PythonWhileStatement(PythonCompoundStatement, LoopAST, WhileAST, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class PythonWhileStatement0(PythonWhileStatement, AST):
    pass


class PythonWhileStatement1(PythonWhileStatement, AST):
    pass


class PythonWhileStatement2(PythonWhileStatement, AST):
    pass


class PythonWhileStatement3(PythonWhileStatement, AST):
    pass


class PythonWildcardImport(PythonAST, AST):
    pass


class PythonWith(PythonAST, TerminalSymbol, AST):
    pass


class PythonWithClause(PythonAST, AST):
    pass


class PythonWithClause0(PythonWithClause, AST):
    pass


class PythonWithClause1(PythonWithClause, AST):
    pass


class PythonWithItem(PythonAST, AST):
    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class PythonWithItem0(PythonWithItem, AST):
    pass


class PythonWithItem1(PythonWithItem, AST):
    pass


class PythonWithStatement(PythonCompoundStatement, AST):
    @_property
    def python_async(self) -> Optional[AST]:
        return self.child_slot("python_async")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class PythonWithStatement0(PythonWithStatement, AST):
    pass


class PythonWithStatement1(PythonWithStatement, AST):
    pass


class PythonYield(PythonAST, AST):
    pass


class PythonYield0(PythonYield, AST):
    pass


class PythonYield1(PythonYield, AST):
    pass


class PythonYield2(PythonYield, AST):
    pass


class PythonYieldTerminal(PythonAST, TerminalSymbol, AST):
    pass


class PythonOpenBracket(PythonAST, TerminalSymbol, AST):
    pass


class PythonCloseBracket(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseXor(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseXorAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonOpenBrace(PythonAST, TerminalSymbol, AST):
    pass


class PythonDoubleOpenBrace(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseOr(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseOrAssign(PythonAST, TerminalSymbol, AST):
    pass


class PythonCloseBrace(PythonAST, TerminalSymbol, AST):
    pass


class PythonDoubleCloseBrace(PythonAST, TerminalSymbol, AST):
    pass


class PythonBitwiseNot(PythonAST, TerminalSymbol, AST):
    pass


class RustAST(CLikeSyntaxAST, NormalScopeAST, AST):
    pass


class RustLogicalNot(RustAST, TerminalSymbol, AST):
    pass


class RustNotEqual(RustAST, TerminalSymbol, AST):
    pass


class RustDoubleQuote(RustAST, TerminalSymbol, AST):
    pass


class RustHashSign(RustAST, TerminalSymbol, AST):
    pass


class RustDollarSign(RustAST, TerminalSymbol, AST):
    pass


class RustModulo(RustAST, TerminalSymbol, AST):
    pass


class RustModuleAssign(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseAnd(RustAST, TerminalSymbol, AST):
    pass


class RustLogicalAnd(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseAndAssign(RustAST, TerminalSymbol, AST):
    pass


class RustSingleQuote(RustAST, TerminalSymbol, AST):
    pass


class RustOpenParenthesis(RustAST, TerminalSymbol, AST):
    pass


class RustCloseParenthesis(RustAST, TerminalSymbol, AST):
    pass


class RustMultiply(RustAST, TerminalSymbol, AST):
    pass


class RustMultiplyAssign(RustAST, TerminalSymbol, AST):
    pass


class RustAdd(RustAST, TerminalSymbol, AST):
    pass


class RustAddAssign(RustAST, TerminalSymbol, AST):
    pass


class RustComma(RustAST, TerminalSymbol, AST):
    pass


class RustSubtract(RustAST, TerminalSymbol, AST):
    pass


class RustSubtractAssign(RustAST, TerminalSymbol, AST):
    pass


class RustDashArrow(RustAST, TerminalSymbol, AST):
    pass


class RustDeclarationStatement(StatementAST, RustAST, AST):
    pass


class RustExpression(ExpressionAST, RustAST, AST):
    pass


class RustLiteral(RustExpression, AST):
    pass


class RustPattern(RustAST, AST):
    pass


class RustLiteralPattern(RustPattern, AST):
    pass


class RustStringContent(RustAST, AST):
    pass


class RustType(TypeAST, RustAST, AST):
    pass


class RustDot(RustAST, TerminalSymbol, AST):
    pass


class RustDotDot(RustAST, TerminalSymbol, AST):
    pass


class RustEllipsis(RustAST, TerminalSymbol, AST):
    pass


class RustDotDotAssign(RustAST, TerminalSymbol, AST):
    pass


class RustDivide(RustAST, TerminalSymbol, AST):
    pass


class RustDivideAssign(RustAST, TerminalSymbol, AST):
    pass


class RustColon(RustAST, TerminalSymbol, AST):
    pass


class RustScopeResolution(RustAST, TerminalSymbol, AST):
    pass


class RustSemicolon(RustAST, TerminalSymbol, AST):
    pass


class RustLessThan(RustAST, TerminalSymbol, AST):
    pass


class RustBitshiftLeft(RustAST, TerminalSymbol, AST):
    pass


class RustBitshiftLeftAssign(RustAST, TerminalSymbol, AST):
    pass


class RustLessThanOrEqual(RustAST, TerminalSymbol, AST):
    pass


class RustAssign(RustAST, TerminalSymbol, AST):
    pass


class RustEqual(RustAST, TerminalSymbol, AST):
    pass


class RustEqualArrow(RustAST, TerminalSymbol, AST):
    pass


class RustGreaterThan(RustAST, TerminalSymbol, AST):
    pass


class RustGreaterThanOrEqual(RustAST, TerminalSymbol, AST):
    pass


class RustBitshiftRight(RustAST, TerminalSymbol, AST):
    pass


class RustBitshiftRightAssign(RustAST, TerminalSymbol, AST):
    pass


class RustQuestion(RustAST, TerminalSymbol, AST):
    pass


class RustMatrixMultiply(RustAST, TerminalSymbol, AST):
    pass


class RustAbstractType(RustType, AST):
    @_property
    def trait(self) -> Optional[AST]:
        return self.child_slot("trait")  # type: ignore


class RustArguments(ArgumentsAST, RustAST, AST):
    pass


class RustArguments0(RustArguments, AST):
    pass


class RustArguments1(RustArguments, AST):
    pass


class RustArguments2(RustArguments, AST):
    pass


class RustArguments3(RustArguments, AST):
    pass


class RustArrayExpression(RustExpression, AST):
    @_property
    def length(self) -> Optional[AST]:
        return self.child_slot("length")  # type: ignore


class RustArrayExpression0(RustArrayExpression, AST):
    pass


class RustArrayExpression1(RustArrayExpression, AST):
    pass


class RustArrayExpression2(RustArrayExpression, AST):
    pass


class RustArrayExpression3(RustArrayExpression, AST):
    pass


class RustArrayExpression4(RustArrayExpression, AST):
    pass


class RustArrayType(RustType, AST):
    @_property
    def length(self) -> Optional[AST]:
        return self.child_slot("length")  # type: ignore

    @_property
    def element(self) -> Optional[AST]:
        return self.child_slot("element")  # type: ignore


class RustArrayType0(RustArrayType, AST):
    pass


class RustArrayType1(RustArrayType, AST):
    pass


class RustAs(RustAST, TerminalSymbol, AST):
    pass


class RustAssignmentExpression(RustExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class RustAssociatedType(RustDeclarationStatement, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def bounds(self) -> Optional[AST]:
        return self.child_slot("bounds")  # type: ignore


class RustAsync(RustAST, TerminalSymbol, AST):
    pass


class RustAsyncBlock(RustExpression, AST):
    pass


class RustAsyncBlock0(RustAsyncBlock, AST):
    pass


class RustAsyncBlock1(RustAsyncBlock, AST):
    pass


class RustAttrItem(RustAST, AST):
    pass


class RustAttributeItem(RustDeclarationStatement, AST):
    pass


class RustAttributeItem0(RustAttributeItem, AST):
    pass


class RustAttributeItem1(RustAttributeItem, AST):
    pass


class RustAwait(RustAST, TerminalSymbol, AST):
    pass


class RustAwaitExpression(RustExpression, AST):
    pass


class RustBaseFieldInitializer(RustAST, AST):
    pass


class RustBinaryExpression(RustExpression, BinaryAST, AST):
    pass


class RustBlock(RustExpression, CompoundAST, AST):
    pass


class RustBlock0(RustBlock, AST):
    pass


class RustBlock1(RustBlock, AST):
    pass


class RustBlockComment(CommentAST, RustAST, AST):
    pass


class RustBlockTerminal(RustExpression, CompoundAST, TerminalSymbol, AST):
    pass


class RustBlot(RustAST, Blot, AST):
    pass


class RustBooleanLiteral(RustLiteralPattern, RustLiteral, BooleanAST, AST):
    pass


class RustBoundedType(RustType, AST):
    pass


class RustBracketedType(RustAST, AST):
    pass


class RustBreak(RustAST, TerminalSymbol, AST):
    pass


class RustBreakExpression(RustExpression, AST):
    pass


class RustBreakExpression0(RustBreakExpression, AST):
    pass


class RustBreakExpression1(RustBreakExpression, AST):
    pass


class RustBreakExpression2(RustBreakExpression, AST):
    pass


class RustBreakExpression3(RustBreakExpression, AST):
    pass


class RustCallExpression(RustExpression, CallAST, AST):
    pass


class RustCapturedPattern(RustPattern, AST):
    pass


class RustCharLiteral(RustLiteralPattern, RustLiteral, AST):
    pass


class RustClosureExpression(RustExpression, AST):
    @_property
    def move(self) -> Optional[AST]:
        return self.child_slot("move")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore


class RustClosureExpression0(RustClosureExpression, AST):
    pass


class RustClosureExpression1(RustClosureExpression, AST):
    pass


class RustClosureExpression2(RustClosureExpression, AST):
    pass


class RustClosureExpression3(RustClosureExpression, AST):
    pass


class RustClosureExpression4(RustClosureExpression, AST):
    pass


class RustClosureExpression5(RustClosureExpression, AST):
    pass


class RustClosureParameters(RustAST, AST):
    pass


class RustClosureParameters0(RustClosureParameters, AST):
    pass


class RustClosureParameters1(RustClosureParameters, AST):
    pass


class RustComment(RustAST, CommentAST, AST):
    pass


class RustCompoundAssignmentExpr(RustExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class RustConst(RustAST, TerminalSymbol, AST):
    pass


class RustConstBlock(RustPattern, RustExpression, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class RustConstItem(RustDeclarationStatement, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustConstItem0(RustConstItem, AST):
    pass


class RustConstItem1(RustConstItem, AST):
    pass


class RustConstItem2(RustConstItem, AST):
    pass


class RustConstItem3(RustConstItem, AST):
    pass


class RustConstParameter(RustAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustConstrainedTypeParameter(RustAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def bounds(self) -> Optional[AST]:
        return self.child_slot("bounds")  # type: ignore


class RustContinue(RustAST, TerminalSymbol, AST):
    pass


class RustContinueExpression(RustExpression, AST):
    pass


class RustContinueExpression0(RustContinueExpression, AST):
    pass


class RustContinueExpression1(RustContinueExpression, AST):
    pass


class RustCrate(RustAST, AST):
    pass


class RustDeclarationList(CompoundAST, RustAST, AST):
    pass


class RustDefault(RustAST, TerminalSymbol, AST):
    pass


class RustDyn(RustAST, TerminalSymbol, AST):
    pass


class RustDynamicType(RustType, AST):
    @_property
    def trait(self) -> Optional[AST]:
        return self.child_slot("trait")  # type: ignore


class RustElse(RustAST, TerminalSymbol, AST):
    pass


class RustElseClause(RustAST, AST):
    pass


class RustEmptyStatement(RustDeclarationStatement, AST):
    pass


class RustEmptyType(RustType, AST):
    pass


class RustEnum(RustAST, TerminalSymbol, AST):
    pass


class RustEnumItem(RustDeclarationStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustEnumItem0(RustEnumItem, AST):
    pass


class RustEnumItem1(RustEnumItem, AST):
    pass


class RustEnumItem2(RustEnumItem, AST):
    pass


class RustEnumItem3(RustEnumItem, AST):
    pass


class RustEnumVariant(RustAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustEnumVariant0(RustEnumVariant, AST):
    pass


class RustEnumVariant1(RustEnumVariant, AST):
    pass


class RustEnumVariant2(RustEnumVariant, AST):
    pass


class RustEnumVariant3(RustEnumVariant, AST):
    pass


class RustEnumVariantList(RustAST, AST):
    pass


class RustEnumVariantList0(RustEnumVariantList, AST):
    pass


class RustEnumVariantList1(RustEnumVariantList, AST):
    pass


class RustEnumVariantList2(RustEnumVariantList, AST):
    pass


class RustEnumVariantList3(RustEnumVariantList, AST):
    pass


class RustError(RustAST, ParseErrorAST, AST):
    pass


class RustErrorTree(ErrorTree, RustAST, AST):
    pass


class RustErrorVariationPoint(ErrorVariationPoint, RustAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class RustErrorVariationPointTree(ErrorVariationPoint, RustAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class RustEscapeSequence(RustAST, AST):
    pass


class RustExpr(RustAST, TerminalSymbol, AST):
    pass


class RustExpressionStatement(StatementAST, RustAST, AST):
    pass


class RustExpressionStatement0(RustExpressionStatement, AST):
    pass


class RustExpressionStatement1(RustExpressionStatement, AST):
    pass


class RustExtern(RustAST, TerminalSymbol, AST):
    pass


class RustExternCrateDeclaration(RustDeclarationStatement, AST):
    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustExternCrateDeclaration0(RustExternCrateDeclaration, AST):
    pass


class RustExternCrateDeclaration1(RustExternCrateDeclaration, AST):
    pass


class RustExternCrateDeclaration2(RustExternCrateDeclaration, AST):
    pass


class RustExternCrateDeclaration3(RustExternCrateDeclaration, AST):
    pass


class RustExternModifier(RustAST, AST):
    pass


class RustExternModifier0(RustExternModifier, AST):
    pass


class RustExternModifier1(RustExternModifier, AST):
    pass


class RustFalse(RustAST, TerminalSymbol, AST):
    pass


class RustFieldDeclaration(RustAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustFieldDeclaration0(RustFieldDeclaration, AST):
    pass


class RustFieldDeclaration1(RustFieldDeclaration, AST):
    pass


class RustFieldDeclarationList(RustAST, AST):
    pass


class RustFieldDeclarationList0(RustFieldDeclarationList, AST):
    pass


class RustFieldDeclarationList1(RustFieldDeclarationList, AST):
    pass


class RustFieldDeclarationList2(RustFieldDeclarationList, AST):
    pass


class RustFieldDeclarationList3(RustFieldDeclarationList, AST):
    pass


class RustFieldExpression(RustExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def field(self) -> Optional[AST]:
        return self.child_slot("field")  # type: ignore


class RustFieldIdentifier(IdentifierAST, RustAST, AST):
    pass


class RustFieldInitializer(RustAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class RustFieldInitializerList(RustAST, AST):
    pass


class RustFieldInitializerList0(RustFieldInitializerList, AST):
    pass


class RustFieldInitializerList1(RustFieldInitializerList, AST):
    pass


class RustFieldInitializerList2(RustFieldInitializerList, AST):
    pass


class RustFieldInitializerList3(RustFieldInitializerList, AST):
    pass


class RustFieldPattern(RustAST, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustFieldPattern0(RustFieldPattern, AST):
    pass


class RustFieldPattern1(RustFieldPattern, AST):
    pass


class RustFieldPattern2(RustFieldPattern, AST):
    pass


class RustFieldPattern3(RustFieldPattern, AST):
    pass


class RustFloatLiteral(RustLiteralPattern, RustLiteral, FloatAST, AST):
    pass


class RustFn(RustAST, TerminalSymbol, AST):
    pass


class RustFor(RustAST, TerminalSymbol, AST):
    pass


class RustForExpression(RustExpression, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class RustForExpression0(RustForExpression, AST):
    pass


class RustForExpression1(RustForExpression, AST):
    pass


class RustForLifetimes(RustAST, AST):
    pass


class RustForeignModItem(RustDeclarationStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class RustForeignModItem0(RustForeignModItem, AST):
    pass


class RustForeignModItem1(RustForeignModItem, AST):
    pass


class RustForeignModItem2(RustForeignModItem, AST):
    pass


class RustForeignModItem3(RustForeignModItem, AST):
    pass


class RustFragmentSpecifier(RustAST, AST):
    pass


class RustFunctionItem(RustDeclarationStatement, FunctionDeclarationAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustFunctionItem0(RustFunctionItem, AST):
    pass


class RustFunctionItem1(RustFunctionItem, AST):
    pass


class RustFunctionItem10(RustFunctionItem, AST):
    pass


class RustFunctionItem11(RustFunctionItem, AST):
    pass


class RustFunctionItem12(RustFunctionItem, AST):
    pass


class RustFunctionItem13(RustFunctionItem, AST):
    pass


class RustFunctionItem14(RustFunctionItem, AST):
    pass


class RustFunctionItem15(RustFunctionItem, AST):
    pass


class RustFunctionItem2(RustFunctionItem, AST):
    pass


class RustFunctionItem3(RustFunctionItem, AST):
    pass


class RustFunctionItem4(RustFunctionItem, AST):
    pass


class RustFunctionItem5(RustFunctionItem, AST):
    pass


class RustFunctionItem6(RustFunctionItem, AST):
    pass


class RustFunctionItem7(RustFunctionItem, AST):
    pass


class RustFunctionItem8(RustFunctionItem, AST):
    pass


class RustFunctionItem9(RustFunctionItem, AST):
    pass


class RustFunctionModifiers(RustAST, AST):
    @_property
    def modifiers(self) -> List[AST]:
        return self.child_slot("modifiers")  # type: ignore


class RustFunctionModifiers0(RustFunctionModifiers, AST):
    pass


class RustFunctionModifiers1(RustFunctionModifiers, AST):
    pass


class RustFunctionModifiers2(RustFunctionModifiers, AST):
    pass


class RustFunctionModifiers3(RustFunctionModifiers, AST):
    pass


class RustFunctionModifiers4(RustFunctionModifiers, AST):
    pass


class RustFunctionSignatureItem(RustDeclarationStatement, AST):
    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustFunctionSignatureItem0(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem1(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem10(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem11(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem12(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem13(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem14(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem15(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem2(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem3(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem4(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem5(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem6(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem7(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem8(RustFunctionSignatureItem, AST):
    pass


class RustFunctionSignatureItem9(RustFunctionSignatureItem, AST):
    pass


class RustFunctionType(RustType, AST):
    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def trait(self) -> Optional[AST]:
        return self.child_slot("trait")  # type: ignore


class RustFunctionType0(RustFunctionType, AST):
    pass


class RustFunctionType1(RustFunctionType, AST):
    pass


class RustFunctionType10(RustFunctionType, AST):
    pass


class RustFunctionType11(RustFunctionType, AST):
    pass


class RustFunctionType2(RustFunctionType, AST):
    pass


class RustFunctionType3(RustFunctionType, AST):
    pass


class RustFunctionType4(RustFunctionType, AST):
    pass


class RustFunctionType5(RustFunctionType, AST):
    pass


class RustFunctionType6(RustFunctionType, AST):
    pass


class RustFunctionType7(RustFunctionType, AST):
    pass


class RustFunctionType8(RustFunctionType, AST):
    pass


class RustFunctionType9(RustFunctionType, AST):
    pass


class RustGenericFunction(RustExpression, AST):
    @_property
    def function(self) -> Optional[AST]:
        return self.child_slot("function")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore


class RustGenericType(RustType, AST):
    @_property
    def turbofish_operator(self) -> Optional[AST]:
        return self.child_slot("turbofish_operator")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustGenericType0(RustGenericType, AST):
    pass


class RustGenericType1(RustGenericType, AST):
    pass


class RustGenericTypeWithTurbofish(RustAST, AST):
    @_property
    def turbofish_operator(self) -> Optional[AST]:
        return self.child_slot("turbofish_operator")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustGenericTypeWithTurbofish0(RustGenericTypeWithTurbofish, AST):
    pass


class RustGenericTypeWithTurbofish1(RustGenericTypeWithTurbofish, AST):
    pass


class RustHigherRankedTraitBound(RustAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustIdent(RustAST, TerminalSymbol, AST):
    pass


class RustIdentifier(RustPattern, RustExpression, IdentifierAST, AST):
    pass


class RustIf(RustAST, TerminalSymbol, AST):
    pass


class RustIfExpression(RustExpression, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class RustIfExpression0(RustIfExpression, AST):
    pass


class RustIfExpression1(RustIfExpression, AST):
    pass


class RustIfLetExpression(RustExpression, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class RustIfLetExpression0(RustIfLetExpression, AST):
    pass


class RustIfLetExpression1(RustIfLetExpression, AST):
    pass


class RustImpl(RustAST, TerminalSymbol, AST):
    pass


class RustImplItem(RustDeclarationStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def trait(self) -> Optional[AST]:
        return self.child_slot("trait")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore


class RustImplItem0(RustImplItem, AST):
    pass


class RustImplItem1(RustImplItem, AST):
    pass


class RustImplItem2(RustImplItem, AST):
    pass


class RustImplItem3(RustImplItem, AST):
    pass


class RustImplItem4(RustImplItem, AST):
    pass


class RustImplItem5(RustImplItem, AST):
    pass


class RustImplItem6(RustImplItem, AST):
    pass


class RustImplItem7(RustImplItem, AST):
    pass


class RustImplicitReturnExpression(ReturnAST, RustAST, AST):
    pass


class RustIn(RustAST, TerminalSymbol, AST):
    pass


class RustIndexExpression(RustExpression, SubscriptAST, AST):
    pass


class RustInnerAttributeItem(RustDeclarationStatement, AST):
    pass


class RustInnerAttributeItem0(RustInnerAttributeItem, AST):
    pass


class RustInnerAttributeItem1(RustInnerAttributeItem, AST):
    pass


class RustInnerWhitespace(RustAST, InnerWhitespace, AST):
    pass


class RustIntegerLiteral(RustLiteralPattern, RustLiteral, IntegerAST, AST):
    pass


class RustItem(RustAST, TerminalSymbol, AST):
    pass


class RustLet(RustAST, TerminalSymbol, AST):
    pass


class RustLetDeclaration(RustDeclarationStatement, VariableDeclarationAST, AST):
    @_property
    def mutable_specifier(self) -> Optional[AST]:
        return self.child_slot("mutable_specifier")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class RustLetDeclaration0(RustLetDeclaration, AST):
    pass


class RustLetDeclaration1(RustLetDeclaration, AST):
    pass


class RustLetDeclaration2(RustLetDeclaration, AST):
    pass


class RustLetDeclaration3(RustLetDeclaration, AST):
    pass


class RustLifetime(RustAST, AST):
    pass


class RustLifetimeTerminal(RustAST, TerminalSymbol, AST):
    pass


class RustLineComment(CommentAST, RustAST, AST):
    pass


class RustLoop(RustAST, TerminalSymbol, AST):
    pass


class RustLoopExpression(RustExpression, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class RustLoopExpression0(RustLoopExpression, AST):
    pass


class RustLoopExpression1(RustLoopExpression, AST):
    pass


class RustLoopLabel(RustAST, AST):
    pass


class RustMacroDefinition(RustDeclarationStatement, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustMacroDefinition0(RustMacroDefinition, AST):
    pass


class RustMacroDefinition1(RustMacroDefinition, AST):
    pass


class RustMacroDefinition2(RustMacroDefinition, AST):
    pass


class RustMacroDefinition3(RustMacroDefinition, AST):
    pass


class RustMacroInvocation(RustPattern, RustDeclarationStatement, RustType, RustExpression, AST):
    @_property
    def macro(self) -> Optional[AST]:
        return self.child_slot("macro")  # type: ignore


class RustMacroRule(RustAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class RustMacroRulesExclamation(RustAST, TerminalSymbol, AST):
    pass


class RustMatch(RustAST, TerminalSymbol, AST):
    pass


class RustMatchArm(RustAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class RustMatchArm0(RustMatchArm, AST):
    pass


class RustMatchArm1(RustMatchArm, AST):
    pass


class RustMatchBlock(RustAST, AST):
    pass


class RustMatchExpression(RustExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class RustMatchPattern(RustAST, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class RustMatchPattern0(RustMatchPattern, AST):
    pass


class RustMatchPattern1(RustMatchPattern, AST):
    pass


class RustMeta(RustAST, TerminalSymbol, AST):
    pass


class RustMetaArguments(RustAST, AST):
    pass


class RustMetaArguments0(RustMetaArguments, AST):
    pass


class RustMetaArguments1(RustMetaArguments, AST):
    pass


class RustMetaArguments2(RustMetaArguments, AST):
    pass


class RustMetaArguments3(RustMetaArguments, AST):
    pass


class RustMetaItem(RustAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class RustMetaItem0(RustMetaItem, AST):
    pass


class RustMetaItem1(RustMetaItem, AST):
    pass


class RustMetavariable(RustType, RustExpression, AST):
    pass


class RustMod(RustAST, TerminalSymbol, AST):
    pass


class RustModItem(RustDeclarationStatement, NamespaceDeclarationAST, AST):
    pass


class RustModItem0(RustModItem, AST):
    pass


class RustModItem1(RustModItem, AST):
    pass


class RustModItem2(RustModItem, AST):
    pass


class RustModItem3(RustModItem, AST):
    pass


class RustMove(RustAST, TerminalSymbol, AST):
    pass


class RustMutPattern(RustPattern, AST):
    pass


class RustMutableSpecifier(RustAST, AST):
    pass


class RustNegativeLiteral(RustLiteralPattern, AST):
    pass


class RustOptionalTypeParameter(RustAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def default_type(self) -> Optional[AST]:
        return self.child_slot("default_type")  # type: ignore


class RustOrPattern(RustPattern, AST):
    pass


class RustOrderedFieldDeclarationList(RustAST, AST):
    @_property
    def type(self) -> List[AST]:
        return self.child_slot("type")  # type: ignore


class RustOrderedFieldDeclarationList0(RustOrderedFieldDeclarationList, AST):
    pass


class RustOrderedFieldDeclarationList1(RustOrderedFieldDeclarationList, AST):
    pass


class RustOrderedFieldDeclarationList2(RustOrderedFieldDeclarationList, AST):
    pass


class RustOrderedFieldDeclarationList3(RustOrderedFieldDeclarationList, AST):
    pass


class RustOrderedFieldDeclarationList4(RustOrderedFieldDeclarationList, AST):
    pass


class RustOrderedFieldDeclarationList5(RustOrderedFieldDeclarationList, AST):
    pass


class RustParameter(ParameterAST, RustAST, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def mutable_specifier(self) -> Optional[AST]:
        return self.child_slot("mutable_specifier")  # type: ignore


class RustParameters(ParametersAST, RustAST, AST):
    pass


class RustParameters0(RustParameters, AST):
    pass


class RustParameters1(RustParameters, AST):
    pass


class RustParameters2(RustParameters, AST):
    pass


class RustParameters3(RustParameters, AST):
    pass


class RustParameters4(RustParameters, AST):
    pass


class RustParameters5(RustParameters, AST):
    pass


class RustParameters6(RustParameters, AST):
    pass


class RustParameters7(RustParameters, AST):
    pass


class RustParameters8(RustParameters, AST):
    pass


class RustParameters9(RustParameters, AST):
    pass


class RustParenthesizedExpression(RustExpression, ParenthesizedExpressionAST, AST):
    pass


class RustPat(RustAST, TerminalSymbol, AST):
    pass


class RustPath(RustAST, TerminalSymbol, AST):
    pass


class RustPointerType(RustType, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustPointerType0(RustPointerType, AST):
    pass


class RustPointerType1(RustPointerType, AST):
    pass


class RustPrimitiveType(RustType, IdentifierAST, AST):
    pass


class RustPub(RustAST, TerminalSymbol, AST):
    pass


class RustQualifiedType(RustAST, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore


class RustRangeExpression(RustExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class RustRangeExpr(RustRangeExpression, AST):
    pass


class RustRangeFromExpr(RustRangeExpression, AST):
    pass


class RustRangeFullExpr(RustRangeExpression, AST):
    pass


class RustRangePattern(RustPattern, AST):
    pass


class RustRangePattern0(RustRangePattern, AST):
    pass


class RustRangePattern1(RustRangePattern, AST):
    pass


class RustRangePattern2(RustRangePattern, AST):
    pass


class RustRangePattern3(RustRangePattern, AST):
    pass


class RustRangePattern4(RustRangePattern, AST):
    pass


class RustRangePattern5(RustRangePattern, AST):
    pass


class RustRangePattern6(RustRangePattern, AST):
    pass


class RustRangePattern7(RustRangePattern, AST):
    pass


class RustRangePattern8(RustRangePattern, AST):
    pass


class RustRangeToExpr(RustRangeExpression, AST):
    pass


class RustRawStringLiteral(RustLiteralPattern, RustLiteral, AST):
    pass


class RustRef(RustAST, TerminalSymbol, AST):
    pass


class RustRefPattern(RustPattern, AST):
    pass


class RustReferenceExpression(RustExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def mutable_specifier(self) -> Optional[AST]:
        return self.child_slot("mutable_specifier")  # type: ignore


class RustReferencePattern(RustPattern, AST):
    pass


class RustReferencePattern0(RustReferencePattern, AST):
    pass


class RustReferencePattern1(RustReferencePattern, AST):
    pass


class RustReferenceType(RustType, AST):
    @_property
    def mutable_specifier(self) -> Optional[AST]:
        return self.child_slot("mutable_specifier")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustReferenceType0(RustReferenceType, AST):
    pass


class RustReferenceType1(RustReferenceType, AST):
    pass


class RustRemainingFieldPattern(RustPattern, AST):
    pass


class RustRemovedTraitBound(RustAST, AST):
    pass


class RustReturn(RustAST, TerminalSymbol, AST):
    pass


class RustReturnExpression(RustExpression, ReturnAST, AST):
    pass


class RustReturnExpression0(RustReturnExpression, AST):
    pass


class RustReturnExpression1(RustReturnExpression, AST):
    pass


class RustScopedIdentifier(RustPattern, RustExpression, AST):
    @_property
    def path(self) -> Optional[AST]:
        return self.child_slot("path")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustScopedTypeIdentifier(RustType, AST):
    @_property
    def path(self) -> Optional[AST]:
        return self.child_slot("path")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustScopedUseList(RustAST, AST):
    @_property
    def path(self) -> Optional[AST]:
        return self.child_slot("path")  # type: ignore

    @_property
    def list(self) -> Optional[AST]:
        return self.child_slot("list")  # type: ignore


class RustSelf(RustExpression, AST):
    pass


class RustSelfParameter(ParameterAST, RustAST, AST):
    @_property
    def borrow(self) -> Optional[AST]:
        return self.child_slot("borrow")  # type: ignore


class RustSelfParameter0(RustSelfParameter, AST):
    pass


class RustSelfParameter1(RustSelfParameter, AST):
    pass


class RustSelfParameter2(RustSelfParameter, AST):
    pass


class RustSelfParameter3(RustSelfParameter, AST):
    pass


class RustSelfParameter4(RustSelfParameter, AST):
    pass


class RustSelfParameter5(RustSelfParameter, AST):
    pass


class RustSelfParameter6(RustSelfParameter, AST):
    pass


class RustSelfParameter7(RustSelfParameter, AST):
    pass


class RustShorthandFieldIdentifier(RustAST, AST):
    pass


class RustShorthandFieldInitializer(RustAST, AST):
    pass


class RustSlicePattern(RustPattern, AST):
    pass


class RustSlicePattern0(RustSlicePattern, AST):
    pass


class RustSlicePattern1(RustSlicePattern, AST):
    pass


class RustSlicePattern2(RustSlicePattern, AST):
    pass


class RustSlicePattern3(RustSlicePattern, AST):
    pass


class RustSourceFile(RootAST, RustAST, AST):
    pass


class RustSourceTextFragment(RustAST, SourceTextFragment, AST):
    pass


class RustSourceTextFragmentTree(ErrorTree, RustAST, AST):
    pass


class RustSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, RustAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class RustSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, RustAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class RustStatic(RustAST, TerminalSymbol, AST):
    pass


class RustStaticItem(RustDeclarationStatement, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustStaticItem0(RustStaticItem, AST):
    pass


class RustStaticItem1(RustStaticItem, AST):
    pass


class RustStaticItem10(RustStaticItem, AST):
    pass


class RustStaticItem11(RustStaticItem, AST):
    pass


class RustStaticItem12(RustStaticItem, AST):
    pass


class RustStaticItem13(RustStaticItem, AST):
    pass


class RustStaticItem14(RustStaticItem, AST):
    pass


class RustStaticItem15(RustStaticItem, AST):
    pass


class RustStaticItem2(RustStaticItem, AST):
    pass


class RustStaticItem3(RustStaticItem, AST):
    pass


class RustStaticItem4(RustStaticItem, AST):
    pass


class RustStaticItem5(RustStaticItem, AST):
    pass


class RustStaticItem6(RustStaticItem, AST):
    pass


class RustStaticItem7(RustStaticItem, AST):
    pass


class RustStaticItem8(RustStaticItem, AST):
    pass


class RustStaticItem9(RustStaticItem, AST):
    pass


class RustStmt(RustAST, TerminalSymbol, AST):
    pass


class RustStringLiteral(RustLiteralPattern, RustLiteral, StringAST, AST):
    pass


class RustStruct(RustAST, TerminalSymbol, AST):
    pass


class RustStructExpression(RustExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class RustStructItem(RustDeclarationStatement, TypeDeclarationAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustStructItem0(RustStructItem, AST):
    pass


class RustStructItem1(RustStructItem, AST):
    pass


class RustStructItem2(RustStructItem, AST):
    pass


class RustStructItem3(RustStructItem, AST):
    pass


class RustStructItem4(RustStructItem, AST):
    pass


class RustStructItem5(RustStructItem, AST):
    pass


class RustStructItem6(RustStructItem, AST):
    pass


class RustStructItem7(RustStructItem, AST):
    pass


class RustStructItem8(RustStructItem, AST):
    pass


class RustStructItem9(RustStructItem, AST):
    pass


class RustStructPattern(RustPattern, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustStructPattern0(RustStructPattern, AST):
    pass


class RustStructPattern1(RustStructPattern, AST):
    pass


class RustStructPattern2(RustStructPattern, AST):
    pass


class RustStructPattern3(RustStructPattern, AST):
    pass


class RustSuper(RustAST, AST):
    pass


class RustTokenBindingPattern(RustAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustTokenRepetition(RustAST, AST):
    pass


class RustTokenRepetitionPattern(RustAST, AST):
    pass


class RustTokenTree(RustAST, AST):
    pass


class RustTokenTreePattern(RustAST, AST):
    pass


class RustTrait(RustAST, TerminalSymbol, AST):
    pass


class RustTraitBounds(RustAST, AST):
    pass


class RustTraitItem(RustDeclarationStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def bounds(self) -> Optional[AST]:
        return self.child_slot("bounds")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustTraitItem0(RustTraitItem, AST):
    pass


class RustTraitItem1(RustTraitItem, AST):
    pass


class RustTraitItem2(RustTraitItem, AST):
    pass


class RustTraitItem3(RustTraitItem, AST):
    pass


class RustTraitItem4(RustTraitItem, AST):
    pass


class RustTraitItem5(RustTraitItem, AST):
    pass


class RustTraitItem6(RustTraitItem, AST):
    pass


class RustTraitItem7(RustTraitItem, AST):
    pass


class RustTrue(RustAST, TerminalSymbol, AST):
    pass


class RustTryExpression(RustExpression, AST):
    pass


class RustTt(RustAST, TerminalSymbol, AST):
    pass


class RustTupleExpression(RustExpression, AST):
    pass


class RustTupleExpression0(RustTupleExpression, AST):
    pass


class RustTupleExpression1(RustTupleExpression, AST):
    pass


class RustTupleExpression2(RustTupleExpression, AST):
    pass


class RustTupleExpression3(RustTupleExpression, AST):
    pass


class RustTuplePattern(RustPattern, AST):
    pass


class RustTuplePattern0(RustTuplePattern, AST):
    pass


class RustTuplePattern1(RustTuplePattern, AST):
    pass


class RustTuplePattern2(RustTuplePattern, AST):
    pass


class RustTuplePattern3(RustTuplePattern, AST):
    pass


class RustTupleStructPattern(RustPattern, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustTupleStructPattern0(RustTupleStructPattern, AST):
    pass


class RustTupleStructPattern1(RustTupleStructPattern, AST):
    pass


class RustTupleStructPattern2(RustTupleStructPattern, AST):
    pass


class RustTupleStructPattern3(RustTupleStructPattern, AST):
    pass


class RustTupleType(RustType, AST):
    pass


class RustTy(RustAST, TerminalSymbol, AST):
    pass


class RustTypeArguments(RustAST, AST):
    pass


class RustTypeBinding(RustAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustTypeCastExpression(RustExpression, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class RustTypeIdentifier(RustType, TypeIdentifierAST, AST):
    pass


class RustTypeItem(RustDeclarationStatement, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustTypeItem0(RustTypeItem, AST):
    pass


class RustTypeItem1(RustTypeItem, AST):
    pass


class RustTypeParameters(RustAST, AST):
    pass


class RustTypeParameters0(RustTypeParameters, AST):
    pass


class RustTypeParameters1(RustTypeParameters, AST):
    pass


class RustUnaryExpression(RustExpression, UnaryAST, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class RustUnion(RustAST, TerminalSymbol, AST):
    pass


class RustUnionItem(RustDeclarationStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class RustUnionItem0(RustUnionItem, AST):
    pass


class RustUnionItem1(RustUnionItem, AST):
    pass


class RustUnionItem2(RustUnionItem, AST):
    pass


class RustUnionItem3(RustUnionItem, AST):
    pass


class RustUnitExpression(RustExpression, AST):
    pass


class RustUnitType(RustType, AST):
    pass


class RustUnsafe(RustAST, TerminalSymbol, AST):
    pass


class RustUnsafeBlock(RustExpression, AST):
    pass


class RustUse(RustAST, TerminalSymbol, AST):
    pass


class RustUseAsClause(RustAST, AST):
    @_property
    def path(self) -> Optional[AST]:
        return self.child_slot("path")  # type: ignore

    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore


class RustUseDeclaration(RustDeclarationStatement, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class RustUseDeclaration0(RustUseDeclaration, AST):
    pass


class RustUseDeclaration1(RustUseDeclaration, AST):
    pass


class RustUseList(RustAST, AST):
    pass


class RustUseList0(RustUseList, AST):
    pass


class RustUseList1(RustUseList, AST):
    pass


class RustUseList2(RustUseList, AST):
    pass


class RustUseList3(RustUseList, AST):
    pass


class RustUseList4(RustUseList, AST):
    pass


class RustUseList5(RustUseList, AST):
    pass


class RustUseList6(RustUseList, AST):
    pass


class RustUseList7(RustUseList, AST):
    pass


class RustUseWildcard(RustAST, AST):
    pass


class RustUseWildcard0(RustUseWildcard, AST):
    pass


class RustUseWildcard1(RustUseWildcard, AST):
    pass


class RustUseWildcard2(RustUseWildcard, AST):
    pass


class RustVariadicParameter(RustAST, AST):
    pass


class RustVis(RustAST, TerminalSymbol, AST):
    pass


class RustVisibilityModifier(RustAST, AST):
    pass


class RustVisibilityModifier0(RustVisibilityModifier, AST):
    pass


class RustVisibilityModifier1(RustVisibilityModifier, AST):
    pass


class RustWhere(RustAST, TerminalSymbol, AST):
    pass


class RustWhereClause(RustAST, AST):
    pass


class RustWherePredicate(RustAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def bounds(self) -> Optional[AST]:
        return self.child_slot("bounds")  # type: ignore


class RustWhile(RustAST, TerminalSymbol, AST):
    pass


class RustWhileExpression(RustExpression, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class RustWhileExpression0(RustWhileExpression, AST):
    pass


class RustWhileExpression1(RustWhileExpression, AST):
    pass


class RustWhileLetExpression(RustExpression, LoopAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore


class RustWhileLetExpression0(RustWhileLetExpression, AST):
    pass


class RustWhileLetExpression1(RustWhileLetExpression, AST):
    pass


class RustYield(RustAST, TerminalSymbol, AST):
    pass


class RustYieldExpression(RustExpression, AST):
    pass


class RustYieldExpression0(RustYieldExpression, AST):
    pass


class RustYieldExpression1(RustYieldExpression, AST):
    pass


class RustOpenBracket(RustAST, TerminalSymbol, AST):
    pass


class RustCloseBracket(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseXor(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseXorAssign(RustAST, TerminalSymbol, AST):
    pass


class Rust_(RustPattern, AST):
    pass


class RustOpenBrace(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseOr(RustAST, TerminalSymbol, AST):
    pass


class RustBitwiseOrAssign(RustAST, TerminalSymbol, AST):
    pass


class RustLogicalOr(RustAST, TerminalSymbol, AST):
    pass


class RustCloseBrace(RustAST, TerminalSymbol, AST):
    pass


class TypescriptAST(ECMAAST, AST):
    pass


class TypescriptTsAST(TypescriptAST, CLikeSyntaxAST, AST):
    pass


class TypescriptTsLogicalNot(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNotEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsStrictlyNotEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDoubleQuote(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOpenTemplateLiteral(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsModulo(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsModuleAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseAnd(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLogicalAnd(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLogicalAndAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseAndAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsSingleQuote(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOpenParenthesis(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsCloseParenthesis(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsMultiply(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsPow(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsPowAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsMultiplyAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAdd(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsIncrement(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAddAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsComma(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsSubtract(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDecrement(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsSubtractAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOmittingTypeTerminal(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAutomaticSemicolon(TypescriptTsAST, AST):
    pass


class TypescriptTsFunctionSignatureAutomaticSemicolon(TypescriptTsAST, AST):
    pass


class TypescriptTsPrimaryType(TypescriptTsAST, AST):
    pass


class TypescriptTsTemplateChars(TypescriptTsAST, AST):
    pass


class TypescriptTsTernaryQmark(TypescriptTsAST, AST):
    pass


class TypescriptTsDot(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsEllipsis(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDivide(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDivideAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsColon(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsSemicolon(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLessThan(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitshiftLeft(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitshiftLeftAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLessThanOrEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsStrictlyEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsEqualArrow(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsGreaterThan(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsGreaterThanOrEqual(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitshiftRight(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitshiftRightAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsUnsignedBitshiftRight(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsUnsignedBitshiftRightAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsQuestion(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsChaining(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOptingTypeTerminal(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNullishCoalescing(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNullishCoalescingAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsMatrixMultiply(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAbstract(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsStatement(TypescriptTsAST, AST):
    pass


class TypescriptTsDeclaration(TypescriptTsStatement, AST):
    pass


class TypescriptTsAbstractClassDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class TypescriptTsAbstractClassDeclaration0(TypescriptTsAbstractClassDeclaration, AST):
    pass


class TypescriptTsAbstractClassDeclaration1(TypescriptTsAbstractClassDeclaration, AST):
    pass


class TypescriptTsAbstractMethodSignature(TypescriptTsAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsAbstractMethodSignature0(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature1(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature2(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature3(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature4(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature5(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature6(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAbstractMethodSignature7(TypescriptTsAbstractMethodSignature, AST):
    pass


class TypescriptTsAccessibilityModifier(TypescriptTsAST, AST):
    pass


class TypescriptTsAmbientDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsAmbientDeclaration0(TypescriptTsAmbientDeclaration, AST):
    pass


class TypescriptTsAmbientDeclaration1(TypescriptTsAmbientDeclaration, AST):
    pass


class TypescriptTsAmbientDeclaration2(TypescriptTsAmbientDeclaration, AST):
    pass


class TypescriptTsAny(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsArguments(ECMAArguments, TypescriptTsAST, AST):
    pass


class TypescriptTsArguments0(TypescriptTsArguments, AST):
    pass


class TypescriptTsArguments1(TypescriptTsArguments, AST):
    pass


class TypescriptTsArguments2(TypescriptTsArguments, AST):
    pass


class TypescriptTsExpression(TypescriptTsAST, AST):
    pass


class TypescriptTsPrimaryExpression(TypescriptTsExpression, AST):
    pass


class TypescriptTsArray(TypescriptTsPrimaryExpression, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsArray0(TypescriptTsArray, AST):
    pass


class TypescriptTsArray1(TypescriptTsArray, AST):
    pass


class TypescriptTsArray2(TypescriptTsArray, AST):
    pass


class TypescriptTsPattern(TypescriptTsAST, AST):
    pass


class TypescriptTsArrayPattern(TypescriptTsPattern, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsArrayPattern0(TypescriptTsArrayPattern, AST):
    pass


class TypescriptTsArrayPattern1(TypescriptTsArrayPattern, AST):
    pass


class TypescriptTsArrayPattern2(TypescriptTsArrayPattern, AST):
    pass


class TypescriptArrayType(AST):
    pass


class TypescriptTsArrayType(TypescriptTsPrimaryType, TypescriptArrayType, AST):
    pass


class TypescriptTsArrowFunction(TypescriptTsPrimaryExpression, LambdaAST, AST):
    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore


class TypescriptTsArrowFunction0(TypescriptTsArrowFunction, AST):
    pass


class TypescriptTsArrowFunction1(TypescriptTsArrowFunction, AST):
    pass


class TypescriptTsAs(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAsExpression(TypescriptTsExpression, AST):
    pass


class TypescriptTsAsExpression0(TypescriptTsAsExpression, AST):
    pass


class TypescriptTsAsExpression1(TypescriptTsAsExpression, AST):
    pass


class TypescriptTsAsserts(TypescriptTsAST, AST):
    pass


class TypescriptTsAssertsTerminal(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptAssignmentExpression(AST):
    pass


class TypescriptTsAssignmentExpression(TypescriptTsExpression, TypescriptAssignmentExpression, AssignmentAST, ECMAAssignmentExpression, AST):
    pass


class TypescriptAssignmentPattern(AST):
    pass


class TypescriptTsAssignmentPattern(TypescriptAssignmentPattern, AssignmentAST, ECMAAssignmentPattern, TypescriptTsAST, AST):
    pass


class TypescriptTsAsync(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAugmentedAssignmentExpression(TypescriptTsExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsAwait(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsAwaitExpression(TypescriptTsExpression, AST):
    pass


class TypescriptTsBinaryExpression(TypescriptTsExpression, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsBlot(TypescriptTsAST, Blot, AST):
    pass


class TypescriptTsBoolean(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBreak(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBreakStatement(TypescriptTsStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsCallExpression(TypescriptTsPrimaryExpression, CallAST, ECMACallExpression, AST):
    pass


class TypescriptTsCallExpression0(TypescriptTsCallExpression, AST):
    pass


class TypescriptTsCallExpression1(TypescriptTsCallExpression, AST):
    pass


class TypescriptTsCallExpression2(TypescriptTsCallExpression, AST):
    pass


class TypescriptTsCallSignature(TypescriptTsAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore


class TypescriptTsCase(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsCatch(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsCatchClause(TypescriptTsAST, AST):
    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsCatchClause0(TypescriptTsCatchClause, AST):
    pass


class TypescriptTsCatchClause1(TypescriptTsCatchClause, AST):
    pass


class TypescriptTsCatchClause2(TypescriptTsCatchClause, AST):
    pass


class TypescriptTsClass(TypescriptTsPrimaryExpression, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class TypescriptTsClass0(TypescriptTsClass, AST):
    pass


class TypescriptTsClass1(TypescriptTsClass, AST):
    pass


class TypescriptTsClassBody(TypescriptTsAST, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsClassDeclaration(TypescriptTsDeclaration, ClassAST, AST):
    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore


class TypescriptTsClassDeclaration0(TypescriptTsClassDeclaration, AST):
    pass


class TypescriptTsClassDeclaration1(TypescriptTsClassDeclaration, AST):
    pass


class TypescriptTsClassHeritage(TypescriptTsAST, AST):
    pass


class TypescriptTsClassHeritage0(TypescriptTsClassHeritage, AST):
    pass


class TypescriptTsClassHeritage1(TypescriptTsClassHeritage, AST):
    pass


class TypescriptTsClassTerminal(TypescriptTsPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsComment(ECMAComment, TypescriptTsAST, AST):
    pass


class TypescriptTsComputedPropertyName(TypescriptTsAST, AST):
    pass


class TypescriptTsConditionalType(TypescriptTsPrimaryType, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class TypescriptTsConst(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsConstraint(TypescriptTsAST, AST):
    pass


class TypescriptTsConstructSignature(TypescriptTsAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsConstructorType(TypescriptTsAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsContinue(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsContinueStatement(TypescriptTsStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsDebugger(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDebuggerStatement(TypescriptTsStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsDeclare(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDecorator(TypescriptTsAST, AST):
    pass


class TypescriptTsDecorator0(TypescriptTsDecorator, AST):
    pass


class TypescriptTsDecorator1(TypescriptTsDecorator, AST):
    pass


class TypescriptTsDecorator2(TypescriptTsDecorator, AST):
    pass


class TypescriptTsDefault(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDefaultType(TypescriptTsAST, AST):
    pass


class TypescriptTsDelete(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDo(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsDoStatement(TypescriptTsStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsElse(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsElseClause(TypescriptTsAST, AST):
    pass


class TypescriptTsEmptyStatement(TypescriptTsStatement, AST):
    pass


class TypescriptTsEnum(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsEnumAssignment(TypescriptTsAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsEnumBody(TypescriptTsAST, AST):
    @_property
    def name(self) -> List[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsEnumBody0(TypescriptTsEnumBody, AST):
    pass


class TypescriptTsEnumBody1(TypescriptTsEnumBody, AST):
    pass


class TypescriptTsEnumBody2(TypescriptTsEnumBody, AST):
    pass


class TypescriptTsEnumBody3(TypescriptTsEnumBody, AST):
    pass


class TypescriptTsEnumBody4(TypescriptTsEnumBody, AST):
    pass


class TypescriptTsEnumDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore


class TypescriptTsError(TypescriptTsAST, ECMAError, ParseErrorAST, AST):
    pass


class TypescriptTsErrorTree(ErrorTree, TypescriptTsAST, AST):
    pass


class TypescriptTsErrorVariationPoint(ErrorVariationPoint, TypescriptTsAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class TypescriptTsErrorVariationPointTree(ErrorVariationPoint, TypescriptTsAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class TypescriptTsEscapeSequence(TypescriptTsAST, AST):
    pass


class TypescriptTsExistentialType(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsExport(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsExportClause(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsExportClause0(TypescriptTsExportClause, AST):
    pass


class TypescriptTsExportClause1(TypescriptTsExportClause, AST):
    pass


class TypescriptTsExportClause2(TypescriptTsExportClause, AST):
    pass


class TypescriptTsExportClause3(TypescriptTsExportClause, AST):
    pass


class TypescriptTsExportSpecifier(TypescriptTsAST, AST):
    pass


class TypescriptTsExportStatement(TypescriptTsStatement, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def declaration(self) -> Optional[AST]:
        return self.child_slot("declaration")  # type: ignore

    @_property
    def default(self) -> Optional[AST]:
        return self.child_slot("default")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsExportStatement0(TypescriptTsExportStatement, AST):
    pass


class TypescriptTsExportStatement1(TypescriptTsExportStatement, AST):
    pass


class TypescriptTsExportStatement2(TypescriptTsExportStatement, AST):
    pass


class TypescriptTsExpressionStatement(TypescriptTsStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsExtends(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsExtendsClause(TypescriptTsAST, AST):
    @_property
    def type_arguments(self) -> List[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def value(self) -> List[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsExtendsTypeClause(TypescriptTsAST, AST):
    @_property
    def type(self) -> List[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsFalse(TypescriptTsPrimaryExpression, BooleanFalseAST, AST):
    pass


class TypescriptTsFinally(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsFinallyClause(TypescriptTsAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptFlowMaybeType(AST):
    pass


class TypescriptTsFlowMaybeType(TypescriptTsPrimaryType, TypescriptFlowMaybeType, AST):
    pass


class TypescriptTsFor(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsForInStatement(TypescriptTsStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore


class TypescriptTsForInStatement0(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement1(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement2(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement3(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement4(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement5(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement6(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForInStatement7(TypescriptTsForInStatement, AST):
    pass


class TypescriptTsForStatement(TypescriptTsStatement, AST):
    @_property
    def initializer(self) -> Optional[AST]:
        return self.child_slot("initializer")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def increment(self) -> Optional[AST]:
        return self.child_slot("increment")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsFormalParameters(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsFormalParameters0(TypescriptTsFormalParameters, AST):
    pass


class TypescriptTsFormalParameters1(TypescriptTsFormalParameters, AST):
    pass


class TypescriptTsFormalParameters2(TypescriptTsFormalParameters, AST):
    pass


class TypescriptTsFrom(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsFunction(TypescriptTsPrimaryExpression, FunctionAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore


class TypescriptFunctionDeclaration(AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsFunctionDeclaration(TypescriptTsDeclaration, TypescriptFunctionDeclaration, FunctionDeclarationAST, AST):
    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore


class TypescriptFunctionSignature(AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsFunctionSignature(TypescriptTsDeclaration, TypescriptFunctionSignature, FunctionDeclarationAST, AST):
    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore


class TypescriptTsFunctionSignature0(TypescriptTsFunctionSignature, AST):
    pass


class TypescriptTsFunctionSignature1(TypescriptTsFunctionSignature, AST):
    pass


class TypescriptTsFunctionTerminal(TypescriptTsPrimaryExpression, FunctionAST, TerminalSymbol, AST):
    pass


class TypescriptTsFunctionType(TypescriptTsAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore


class TypescriptTsGeneratorFunction(TypescriptTsPrimaryExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsGeneratorFunctionDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore


class TypescriptGenericType(AST):
    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsGenericType(TypescriptTsPrimaryType, TypescriptGenericType, AST):
    pass


class TypescriptTsGet(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsGlobal(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsHashBangLine(TypescriptTsAST, AST):
    pass


class TypescriptIdentifier(AST):
    pass


class TypescriptTsIdentifier(TypescriptTsPattern, TypescriptTsPrimaryExpression, TypescriptIdentifier, IdentifierAST, AST):
    pass


class TypescriptTsIf(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsIfStatement(TypescriptTsStatement, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class TypescriptTsIfStatement0(TypescriptTsIfStatement, AST):
    pass


class TypescriptTsIfStatement1(TypescriptTsIfStatement, AST):
    pass


class TypescriptTsImplements(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsImplementsClause(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsImport(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsImportAlias(TypescriptTsDeclaration, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsImportClause(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsImportClause0(TypescriptTsImportClause, AST):
    pass


class TypescriptTsImportClause1(TypescriptTsImportClause, AST):
    pass


class TypescriptTsImportClause2(TypescriptTsImportClause, AST):
    pass


class TypescriptTsImportRequireClause(TypescriptTsAST, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore


class TypescriptTsImportSpecifier(TypescriptTsAST, AST):
    pass


class TypescriptTsImportStatement(TypescriptTsStatement, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsImportStatement0(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement1(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement2(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement3(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement4(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement5(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement6(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement7(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportStatement8(TypescriptTsImportStatement, AST):
    pass


class TypescriptTsImportTerminal(TypescriptTsPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsIn(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptIndexSignature(AST):
    @_property
    def sign(self) -> Optional[AST]:
        return self.child_slot("sign")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def index_type(self) -> Optional[AST]:
        return self.child_slot("index_type")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsIndexSignature(TypescriptIndexSignature, TypescriptTsAST, AST):
    pass


class TypescriptTsIndexSignature0(TypescriptTsIndexSignature, AST):
    pass


class TypescriptTsIndexSignature1(TypescriptTsIndexSignature, AST):
    pass


class TypescriptTsIndexSignature2(TypescriptTsIndexSignature, AST):
    pass


class TypescriptTsIndexSignature3(TypescriptTsIndexSignature, AST):
    pass


class TypescriptTsIndexTypeQuery(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsInfer(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsInferType(TypescriptTsAST, AST):
    pass


class TypescriptTsInnerWhitespace(TypescriptTsAST, InnerWhitespace, AST):
    pass


class TypescriptTsInstanceof(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsInterface(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsInterfaceDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsInterfaceDeclaration0(TypescriptTsInterfaceDeclaration, AST):
    pass


class TypescriptTsInterfaceDeclaration1(TypescriptTsInterfaceDeclaration, AST):
    pass


class TypescriptTsInternalModule(TypescriptTsExpression, TypescriptTsDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptIntersectionType(AST):
    pass


class TypescriptTsIntersectionType(TypescriptTsPrimaryType, TypescriptIntersectionType, AST):
    pass


class TypescriptTsIntersectionType0(TypescriptTsIntersectionType, AST):
    pass


class TypescriptTsIntersectionType1(TypescriptTsIntersectionType, AST):
    pass


class TypescriptTsIs(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsJsxAttribute(TypescriptTsAST, AST):
    pass


class TypescriptTsJsxAttribute0(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxAttribute1(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxAttribute2(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxAttribute3(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxAttribute4(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxAttribute5(TypescriptTsJsxAttribute, AST):
    pass


class TypescriptTsJsxClosingElement(TypescriptTsAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsJsxElement(TypescriptTsAST, AST):
    @_property
    def open_tag(self) -> Optional[AST]:
        return self.child_slot("open_tag")  # type: ignore

    @_property
    def close_tag(self) -> Optional[AST]:
        return self.child_slot("close_tag")  # type: ignore


class TypescriptTsJsxExpression(TypescriptTsAST, AST):
    pass


class TypescriptTsJsxExpression0(TypescriptTsJsxExpression, AST):
    pass


class TypescriptTsJsxExpression1(TypescriptTsJsxExpression, AST):
    pass


class TypescriptTsJsxFragment(TypescriptTsAST, AST):
    pass


class TypescriptTsJsxNamespaceName(TypescriptTsAST, AST):
    pass


class TypescriptTsJsxOpeningElement(TypescriptTsAST, AST):
    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsJsxOpeningElement0(TypescriptTsJsxOpeningElement, AST):
    pass


class TypescriptTsJsxOpeningElement1(TypescriptTsJsxOpeningElement, AST):
    pass


class TypescriptTsJsxSelfClosingElement(TypescriptTsAST, AST):
    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsJsxSelfClosingElement0(TypescriptTsJsxSelfClosingElement, AST):
    pass


class TypescriptTsJsxSelfClosingElement1(TypescriptTsJsxSelfClosingElement, AST):
    pass


class TypescriptTsJsxText(TypescriptTsAST, AST):
    pass


class TypescriptTsKeyof(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLabeledStatement(TypescriptTsStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsLet(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLexicalDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptLiteralType(AST):
    pass


class TypescriptTsLiteralType(TypescriptTsPrimaryType, TypescriptLiteralType, AST):
    pass


class TypescriptTsLiteralType0(TypescriptTsLiteralType, AST):
    pass


class TypescriptTsLiteralType1(TypescriptTsLiteralType, AST):
    pass


class TypescriptTsLookupType(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsMappedTypeClause(TypescriptTsAST, AST):
    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsMappedTypeClause0(TypescriptTsMappedTypeClause, AST):
    pass


class TypescriptTsMappedTypeClause1(TypescriptTsMappedTypeClause, AST):
    pass


class TypescriptTsMemberExpression(TypescriptTsPattern, TypescriptTsPrimaryExpression, ECMAMemberExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class TypescriptTsMemberExpression0(TypescriptTsMemberExpression, AST):
    pass


class TypescriptTsMemberExpression1(TypescriptTsMemberExpression, AST):
    pass


class TypescriptTsMemberExpression2(TypescriptTsMemberExpression, AST):
    pass


class TypescriptTsMetaProperty(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsMethodDefinition(TypescriptTsAST, AST):
    @_property
    def typescript_ts_async(self) -> Optional[AST]:
        return self.child_slot("typescript_ts_async")  # type: ignore

    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def getter_setter(self) -> Optional[AST]:
        return self.child_slot("getter_setter")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsMethodDefinition0(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition1(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition10(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition11(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition12(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition13(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition14(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition15(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition2(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition3(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition4(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition5(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition6(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition7(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition8(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodDefinition9(TypescriptTsMethodDefinition, AST):
    pass


class TypescriptTsMethodSignature(TypescriptTsAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsMethodSignature0(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature1(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature10(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature100(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature101(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature102(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature103(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature104(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature105(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature106(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature107(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature108(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature109(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature11(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature110(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature111(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature112(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature113(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature114(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature115(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature116(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature117(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature118(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature119(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature12(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature120(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature121(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature122(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature123(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature124(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature125(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature126(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature127(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature13(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature14(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature15(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature16(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature17(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature18(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature19(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature2(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature20(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature21(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature22(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature23(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature24(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature25(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature26(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature27(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature28(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature29(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature3(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature30(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature31(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature32(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature33(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature34(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature35(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature36(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature37(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature38(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature39(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature4(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature40(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature41(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature42(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature43(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature44(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature45(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature46(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature47(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature48(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature49(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature5(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature50(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature51(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature52(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature53(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature54(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature55(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature56(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature57(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature58(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature59(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature6(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature60(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature61(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature62(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature63(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature64(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature65(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature66(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature67(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature68(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature69(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature7(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature70(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature71(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature72(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature73(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature74(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature75(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature76(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature77(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature78(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature79(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature8(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature80(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature81(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature82(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature83(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature84(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature85(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature86(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature87(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature88(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature89(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature9(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature90(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature91(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature92(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature93(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature94(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature95(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature96(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature97(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature98(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsMethodSignature99(TypescriptTsMethodSignature, AST):
    pass


class TypescriptTsModule(TypescriptTsDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsModuleTerminal(TypescriptTsDeclaration, TerminalSymbol, AST):
    pass


class TypescriptTsNamedImports(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsNamedImports0(TypescriptTsNamedImports, AST):
    pass


class TypescriptTsNamedImports1(TypescriptTsNamedImports, AST):
    pass


class TypescriptTsNamedImports2(TypescriptTsNamedImports, AST):
    pass


class TypescriptTsNamedImports3(TypescriptTsNamedImports, AST):
    pass


class TypescriptTsNamespace(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNamespaceExport(TypescriptTsAST, AST):
    pass


class TypescriptTsNamespaceImport(TypescriptTsAST, AST):
    pass


class TypescriptTsNestedIdentifier(TypescriptTsAST, AST):
    pass


class TypescriptTsNestedTypeIdentifier(TypescriptTsPrimaryType, AST):
    @_property
    def module(self) -> Optional[AST]:
        return self.child_slot("module")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsNever(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNew(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsNewExpression(TypescriptTsExpression, AST):
    @_property
    def constructor(self) -> Optional[AST]:
        return self.child_slot("constructor")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class TypescriptTsNonNullExpression(TypescriptTsPattern, TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsNull(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsNumber(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsObject(TypescriptTsPrimaryExpression, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsObject0(TypescriptTsObject, AST):
    pass


class TypescriptTsObject1(TypescriptTsObject, AST):
    pass


class TypescriptTsObject2(TypescriptTsObject, AST):
    pass


class TypescriptTsObject3(TypescriptTsObject, AST):
    pass


class TypescriptTsObjectAssignmentPattern(TypescriptTsAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsObjectPattern(TypescriptTsPattern, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsObjectPattern0(TypescriptTsObjectPattern, AST):
    pass


class TypescriptTsObjectPattern1(TypescriptTsObjectPattern, AST):
    pass


class TypescriptTsObjectPattern2(TypescriptTsObjectPattern, AST):
    pass


class TypescriptTsObjectPattern3(TypescriptTsObjectPattern, AST):
    pass


class TypescriptTsObjectTerminal(TypescriptTsPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptObjectType(AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsObjectType(TypescriptTsPrimaryType, TypescriptObjectType, AST):
    pass


class TypescriptTsObjectType0(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType1(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType10(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType11(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType12(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType13(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType14(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType15(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType16(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType17(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType18(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType19(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType2(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType3(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType4(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType5(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType6(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType7(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType8(TypescriptTsObjectType, AST):
    pass


class TypescriptTsObjectType9(TypescriptTsObjectType, AST):
    pass


class TypescriptTsOf(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOmittingTypeAnnotation(TypescriptTsAST, AST):
    pass


class TypescriptTsOptingTypeAnnotation(TypescriptTsAST, AST):
    pass


class TypescriptParameter(AST):
    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def modifiers(self) -> List[AST]:
        return self.child_slot("modifiers")  # type: ignore


class TypescriptOptionalParameter(AST):
    pass


class TypescriptTsOptionalParameter(TypescriptOptionalParameter, TypescriptParameter, ParameterAST, TypescriptTsAST, AST):
    pass


class TypescriptTsOptionalParameter0(TypescriptTsOptionalParameter, AST):
    pass


class TypescriptTsOptionalParameter1(TypescriptTsOptionalParameter, AST):
    pass


class TypescriptTsOptionalType(TypescriptTsAST, AST):
    pass


class TypescriptTsOverride(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOverrideModifier(TypescriptTsAST, AST):
    pass


class TypescriptTsPair(TypescriptTsAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsPairPattern(TypescriptTsAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsParenthesizedExpression(TypescriptTsPrimaryExpression, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsParenthesizedExpression0(TypescriptTsParenthesizedExpression, AST):
    pass


class TypescriptTsParenthesizedExpression1(TypescriptTsParenthesizedExpression, AST):
    pass


class TypescriptTsParenthesizedType(TypescriptTsPrimaryType, AST):
    pass


class TypescriptPredefinedType(AST):
    pass


class TypescriptTsPredefinedType(TypescriptTsPrimaryType, TypescriptPredefinedType, AST):
    pass


class TypescriptTsPrivate(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsPrivatePropertyIdentifier(TypescriptTsAST, AST):
    pass


class TypescriptProgram(AST):
    pass


class TypescriptTsProgram(TypescriptProgram, RootAST, TypescriptTsAST, AST):
    pass


class TypescriptTsProgram0(TypescriptTsProgram, AST):
    pass


class TypescriptTsProgram1(TypescriptTsProgram, AST):
    pass


class TypescriptPropertyIdentifier(AST):
    pass


class TypescriptTsPropertyIdentifier(TypescriptPropertyIdentifier, IdentifierAST, TypescriptTsAST, AST):
    pass


class TypescriptPropertySignature(AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore


class TypescriptTsPropertySignature(TypescriptPropertySignature, TypescriptTsAST, AST):
    pass


class TypescriptTsPropertySignature0(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature1(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature10(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature11(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature12(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature13(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature14(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature15(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature2(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature3(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature4(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature5(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature6(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature7(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature8(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsPropertySignature9(TypescriptTsPropertySignature, AST):
    pass


class TypescriptTsProtected(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsPublic(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsPublicFieldDefinition(TypescriptTsAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def modifiers(self) -> Optional[AST]:
        return self.child_slot("modifiers")  # type: ignore

    @_property
    def declare(self) -> Optional[AST]:
        return self.child_slot("declare")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsPublicFieldDefinition0(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition1(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition10(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition11(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition12(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition13(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition14(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition15(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition16(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition17(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition18(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition19(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition2(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition20(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition21(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition22(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition23(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition24(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition25(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition26(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition27(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition28(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition29(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition3(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition30(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition31(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition32(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition33(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition34(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition35(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition36(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition37(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition38(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition39(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition4(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition40(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition41(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition42(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition43(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition44(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition45(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition46(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition47(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition5(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition6(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition7(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition8(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsPublicFieldDefinition9(TypescriptTsPublicFieldDefinition, AST):
    pass


class TypescriptTsReadonly(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsReadonlyType(TypescriptTsAST, AST):
    pass


class TypescriptTsRegex(TypescriptTsPrimaryExpression, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def flags(self) -> Optional[AST]:
        return self.child_slot("flags")  # type: ignore


class TypescriptTsRegexFlags(TypescriptTsAST, AST):
    pass


class TypescriptTsRegexPattern(TypescriptTsAST, AST):
    pass


class TypescriptTsRequire(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptRequiredParameter(AST):
    pass


class TypescriptTsRequiredParameter(TypescriptRequiredParameter, TypescriptParameter, ParameterAST, TypescriptTsAST, AST):
    pass


class TypescriptTsRequiredParameter0(TypescriptTsRequiredParameter, AST):
    pass


class TypescriptTsRequiredParameter1(TypescriptTsRequiredParameter, AST):
    pass


class TypescriptRestPattern(AST):
    pass


class TypescriptTsRestPattern(TypescriptTsPattern, TypescriptRestPattern, ECMARestPattern, AST):
    pass


class TypescriptTsRestPattern0(TypescriptTsRestPattern, AST):
    pass


class TypescriptTsRestPattern1(TypescriptTsRestPattern, AST):
    pass


class TypescriptTsRestPattern2(TypescriptTsRestPattern, AST):
    pass


class TypescriptTsRestPattern3(TypescriptTsRestPattern, AST):
    pass


class TypescriptTsRestType(TypescriptTsAST, AST):
    pass


class TypescriptTsReturn(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsReturnStatement(TypescriptTsStatement, ReturnAST, AST):
    pass


class TypescriptTsReturnStatement0(TypescriptTsReturnStatement, AST):
    pass


class TypescriptTsReturnStatement1(TypescriptTsReturnStatement, AST):
    pass


class TypescriptTsSequenceExpression(TypescriptTsAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsSet(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsShorthandPropertyIdentifier(IdentifierAST, TypescriptTsAST, AST):
    pass


class TypescriptTsShorthandPropertyIdentifierPattern(IdentifierAST, TypescriptTsAST, AST):
    pass


class TypescriptTsSourceTextFragment(TypescriptTsAST, SourceTextFragment, AST):
    pass


class TypescriptTsSourceTextFragmentTree(ErrorTree, TypescriptTsAST, AST):
    pass


class TypescriptTsSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, TypescriptTsAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class TypescriptTsSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, TypescriptTsAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class TypescriptTsSpreadElement(TypescriptTsAST, AST):
    pass


class TypescriptTsStatementBlock(TypescriptTsStatement, AST):
    pass


class TypescriptTsStatementIdentifier(TypescriptTsAST, AST):
    pass


class TypescriptTsStatic(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsString(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsString0(TypescriptTsString, AST):
    pass


class TypescriptTsString1(TypescriptTsString, AST):
    pass


class TypescriptTsStringFragment(TypescriptTsAST, AST):
    pass


class TypescriptTsStringTerminal(TypescriptTsPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsSubscriptExpression(TypescriptTsPattern, TypescriptTsPrimaryExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def index(self) -> Optional[AST]:
        return self.child_slot("index")  # type: ignore

    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore


class TypescriptTsSubscriptExpression0(TypescriptTsSubscriptExpression, AST):
    pass


class TypescriptTsSubscriptExpression1(TypescriptTsSubscriptExpression, AST):
    pass


class TypescriptTsSuper(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsSwitch(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsSwitchBody(TypescriptTsAST, AST):
    pass


class TypescriptTsSwitchCase(TypescriptTsAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsSwitchDefault(TypescriptTsAST, AST):
    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsSwitchStatement(TypescriptTsStatement, ControlFlowAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsSymbol(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsTarget(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsTemplateLiteralType(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsTemplateString(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsTemplateSubstitution(TypescriptTsAST, AST):
    pass


class TypescriptTsTemplateType(TypescriptTsAST, AST):
    pass


class TypescriptTsTernaryExpression(TypescriptTsExpression, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class TypescriptTsThis(TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptTsThisType(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsThrow(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsThrowStatement(TypescriptTsStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsTrue(TypescriptTsPrimaryExpression, BooleanTrueAST, AST):
    pass


class TypescriptTsTry(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsTryStatement(TypescriptTsStatement, AST):
    @_property
    def finalizer(self) -> Optional[AST]:
        return self.child_slot("finalizer")  # type: ignore

    @_property
    def handler(self) -> Optional[AST]:
        return self.child_slot("handler")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsTryStatement0(TypescriptTsTryStatement, AST):
    pass


class TypescriptTsTryStatement1(TypescriptTsTryStatement, AST):
    pass


class TypescriptTsTryStatement2(TypescriptTsTryStatement, AST):
    pass


class TypescriptTsTryStatement3(TypescriptTsTryStatement, AST):
    pass


class TypescriptTupleType(AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsTupleType(TypescriptTsPrimaryType, TypescriptTupleType, AST):
    pass


class TypescriptTsTupleType0(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType1(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType2(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType3(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType4(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType5(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType6(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType7(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType8(TypescriptTsTupleType, AST):
    pass


class TypescriptTsTupleType9(TypescriptTsTupleType, AST):
    pass


class TypescriptTsType(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsTypeAliasDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTypeAnnotation(AST):
    pass


class TypescriptTsTypeAnnotation(TypescriptTypeAnnotation, TypescriptTsAST, AST):
    pass


class TypescriptTypeArguments(AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsTypeArguments(TypescriptTypeArguments, TypescriptTsAST, AST):
    pass


class TypescriptTsTypeArguments0(TypescriptTsTypeArguments, AST):
    pass


class TypescriptTsTypeArguments1(TypescriptTsTypeArguments, AST):
    pass


class TypescriptTsTypeAssertion(TypescriptTsExpression, AST):
    pass


class TypescriptTypeIdentifier(AST):
    pass


class TypescriptTsTypeIdentifier(TypescriptTsPrimaryType, TypeIdentifierAST, TypescriptTypeIdentifier, AST):
    pass


class TypescriptTsTypeParameter(TypescriptTsAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def constraint(self) -> Optional[AST]:
        return self.child_slot("constraint")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsTypeParameters(TypescriptTsAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsTypeParameters0(TypescriptTsTypeParameters, AST):
    pass


class TypescriptTsTypeParameters1(TypescriptTsTypeParameters, AST):
    pass


class TypescriptTsTypePredicate(TypescriptTsAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsTypePredicateAnnotation(TypescriptTsAST, AST):
    pass


class TypescriptTsTypeQuery(TypescriptTsPrimaryType, AST):
    pass


class TypescriptTsTypeQuery0(TypescriptTsTypeQuery, AST):
    pass


class TypescriptTsTypeQuery1(TypescriptTsTypeQuery, AST):
    pass


class TypescriptTsTypeQuery2(TypescriptTsTypeQuery, AST):
    pass


class TypescriptTsTypeQuery3(TypescriptTsTypeQuery, AST):
    pass


class TypescriptTsTypeof(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsUnaryExpression(TypescriptTsExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class TypescriptTsUndefined(TypescriptTsPattern, TypescriptTsPrimaryExpression, AST):
    pass


class TypescriptUnionType(AST):
    pass


class TypescriptTsUnionType(TypescriptTsPrimaryType, TypescriptUnionType, AST):
    pass


class TypescriptTsUnionType0(TypescriptTsUnionType, AST):
    pass


class TypescriptTsUnionType1(TypescriptTsUnionType, AST):
    pass


class TypescriptTsUnknown(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsUpdateExpression(TypescriptTsExpression, AssignmentAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class TypescriptTsUpdateExpression0(TypescriptTsUpdateExpression, AST):
    pass


class TypescriptTsUpdateExpression1(TypescriptTsUpdateExpression, AST):
    pass


class TypescriptTsVar(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsVariableDeclaration(TypescriptTsDeclaration, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptVariableDeclarator(AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsVariableDeclarator(TypescriptVariableDeclarator, ECMAVariableDeclarator, TypescriptTsAST, AST):
    pass


class TypescriptTsVariableDeclarator0(TypescriptTsVariableDeclarator, AST):
    pass


class TypescriptTsVariableDeclarator1(TypescriptTsVariableDeclarator, AST):
    pass


class TypescriptTsVoid(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsWhile(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsWhileStatement(TypescriptTsStatement, ControlFlowAST, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsWith(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsWithStatement(TypescriptTsStatement, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsYield(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsYieldExpression(TypescriptTsExpression, AST):
    pass


class TypescriptTsYieldExpression0(TypescriptTsYieldExpression, AST):
    pass


class TypescriptTsYieldExpression1(TypescriptTsYieldExpression, AST):
    pass


class TypescriptTsYieldExpression2(TypescriptTsYieldExpression, AST):
    pass


class TypescriptTsOpenBracket(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsCloseBracket(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseXor(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseXorAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBackQuote(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsOpenBrace(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsObjectTypeOpen(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseOr(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseOrAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLogicalOr(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsLogicalOrAssign(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsObjectTypeClose(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsCloseBrace(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsBitwiseNot(TypescriptTsAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAST(TypescriptAST, CLikeSyntaxAST, AST):
    pass


class TypescriptTsxLogicalNot(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNotEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxStrictlyNotEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDoubleQuote(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOpenTemplateLiteral(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxModulo(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxModuleAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseAnd(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLogicalAnd(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLogicalAndAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseAndAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxSingleQuote(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOpenParenthesis(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxCloseParenthesis(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxMultiply(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxPow(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxPowAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxMultiplyAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAdd(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxIncrement(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAddAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxComma(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxSubtract(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDecrement(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxSubtractAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOmittingTypeTerminal(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAutomaticSemicolon(TypescriptTsxAST, AST):
    pass


class TypescriptTsxFunctionSignatureAutomaticSemicolon(TypescriptTsxAST, AST):
    pass


class TypescriptTsxPrimaryType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxTemplateChars(TypescriptTsxAST, AST):
    pass


class TypescriptTsxTernaryQmark(TypescriptTsxAST, AST):
    pass


class TypescriptTsxDot(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxEllipsis(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDivide(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDivideAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxColon(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxSemicolon(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLessThan(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitshiftLeft(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitshiftLeftAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLessThanOrEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxStrictlyEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxEqualArrow(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxGreaterThan(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxGreaterThanOrEqual(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitshiftRight(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitshiftRightAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxUnsignedBitshiftRight(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxUnsignedBitshiftRightAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxQuestion(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxChaining(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOptingTypeTerminal(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNullishCoalescing(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNullishCoalescingAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxMatrixMultiply(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAbstract(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxStatement(TypescriptTsxAST, AST):
    pass


class TypescriptTsxDeclaration(TypescriptTsxStatement, AST):
    pass


class TypescriptTsxAbstractClassDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class TypescriptTsxAbstractClassDeclaration0(TypescriptTsxAbstractClassDeclaration, AST):
    pass


class TypescriptTsxAbstractClassDeclaration1(TypescriptTsxAbstractClassDeclaration, AST):
    pass


class TypescriptTsxAbstractMethodSignature(TypescriptTsxAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxAbstractMethodSignature0(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature1(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature2(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature3(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature4(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature5(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature6(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAbstractMethodSignature7(TypescriptTsxAbstractMethodSignature, AST):
    pass


class TypescriptTsxAccessibilityModifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxAmbientDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxAmbientDeclaration0(TypescriptTsxAmbientDeclaration, AST):
    pass


class TypescriptTsxAmbientDeclaration1(TypescriptTsxAmbientDeclaration, AST):
    pass


class TypescriptTsxAmbientDeclaration2(TypescriptTsxAmbientDeclaration, AST):
    pass


class TypescriptTsxAny(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxArguments(ECMAArguments, TypescriptTsxAST, AST):
    pass


class TypescriptTsxArguments0(TypescriptTsxArguments, AST):
    pass


class TypescriptTsxArguments1(TypescriptTsxArguments, AST):
    pass


class TypescriptTsxArguments2(TypescriptTsxArguments, AST):
    pass


class TypescriptTsxExpression(TypescriptTsxAST, AST):
    pass


class TypescriptTsxPrimaryExpression(TypescriptTsxExpression, AST):
    pass


class TypescriptTsxArray(TypescriptTsxPrimaryExpression, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxArray0(TypescriptTsxArray, AST):
    pass


class TypescriptTsxArray1(TypescriptTsxArray, AST):
    pass


class TypescriptTsxArray2(TypescriptTsxArray, AST):
    pass


class TypescriptTsxPattern(TypescriptTsxAST, AST):
    pass


class TypescriptTsxArrayPattern(TypescriptTsxPattern, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxArrayPattern0(TypescriptTsxArrayPattern, AST):
    pass


class TypescriptTsxArrayPattern1(TypescriptTsxArrayPattern, AST):
    pass


class TypescriptTsxArrayPattern2(TypescriptTsxArrayPattern, AST):
    pass


class TypescriptTsxArrayType(TypescriptTsxPrimaryType, TypescriptArrayType, AST):
    pass


class TypescriptTsxArrowFunction(TypescriptTsxPrimaryExpression, LambdaAST, AST):
    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore


class TypescriptTsxArrowFunction0(TypescriptTsxArrowFunction, AST):
    pass


class TypescriptTsxArrowFunction1(TypescriptTsxArrowFunction, AST):
    pass


class TypescriptTsxAs(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAsExpression(TypescriptTsxExpression, AST):
    pass


class TypescriptTsxAsExpression0(TypescriptTsxAsExpression, AST):
    pass


class TypescriptTsxAsExpression1(TypescriptTsxAsExpression, AST):
    pass


class TypescriptTsxAsserts(TypescriptTsxAST, AST):
    pass


class TypescriptTsxAssertsTerminal(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAssignmentExpression(TypescriptTsxExpression, TypescriptAssignmentExpression, AssignmentAST, ECMAAssignmentExpression, AST):
    pass


class TypescriptTsxAssignmentPattern(TypescriptAssignmentPattern, AssignmentAST, ECMAAssignmentPattern, TypescriptTsxAST, AST):
    pass


class TypescriptTsxAsync(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAugmentedAssignmentExpression(TypescriptTsxExpression, AssignmentAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsxAwait(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxAwaitExpression(TypescriptTsxExpression, AST):
    pass


class TypescriptTsxBinaryExpression(TypescriptTsxExpression, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsxBlot(TypescriptTsxAST, Blot, AST):
    pass


class TypescriptTsxBoolean(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBreak(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBreakStatement(TypescriptTsxStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxCallExpression(TypescriptTsxPrimaryExpression, CallAST, ECMACallExpression, AST):
    pass


class TypescriptTsxCallExpression0(TypescriptTsxCallExpression, AST):
    pass


class TypescriptTsxCallExpression1(TypescriptTsxCallExpression, AST):
    pass


class TypescriptTsxCallExpression2(TypescriptTsxCallExpression, AST):
    pass


class TypescriptTsxCallSignature(TypescriptTsxAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore


class TypescriptTsxCase(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxCatch(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxCatchClause(TypescriptTsxAST, AST):
    @_property
    def parameter(self) -> Optional[AST]:
        return self.child_slot("parameter")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxCatchClause0(TypescriptTsxCatchClause, AST):
    pass


class TypescriptTsxCatchClause1(TypescriptTsxCatchClause, AST):
    pass


class TypescriptTsxCatchClause2(TypescriptTsxCatchClause, AST):
    pass


class TypescriptTsxClass(TypescriptTsxPrimaryExpression, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore


class TypescriptTsxClass0(TypescriptTsxClass, AST):
    pass


class TypescriptTsxClass1(TypescriptTsxClass, AST):
    pass


class TypescriptTsxClassBody(TypescriptTsxAST, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxClassDeclaration(TypescriptTsxDeclaration, ClassAST, AST):
    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore


class TypescriptTsxClassDeclaration0(TypescriptTsxClassDeclaration, AST):
    pass


class TypescriptTsxClassDeclaration1(TypescriptTsxClassDeclaration, AST):
    pass


class TypescriptTsxClassHeritage(TypescriptTsxAST, AST):
    pass


class TypescriptTsxClassHeritage0(TypescriptTsxClassHeritage, AST):
    pass


class TypescriptTsxClassHeritage1(TypescriptTsxClassHeritage, AST):
    pass


class TypescriptTsxClassTerminal(TypescriptTsxPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsxComment(ECMAComment, TypescriptTsxAST, AST):
    pass


class TypescriptTsxComputedPropertyName(TypescriptTsxAST, AST):
    pass


class TypescriptTsxConditionalType(TypescriptTsxPrimaryType, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class TypescriptTsxConst(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxConstraint(TypescriptTsxAST, AST):
    pass


class TypescriptTsxConstructSignature(TypescriptTsxAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsxConstructorType(TypescriptTsxAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsxContinue(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxContinueStatement(TypescriptTsxStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxDebugger(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDebuggerStatement(TypescriptTsxStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxDeclare(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDecorator(TypescriptTsxAST, AST):
    pass


class TypescriptTsxDecorator0(TypescriptTsxDecorator, AST):
    pass


class TypescriptTsxDecorator1(TypescriptTsxDecorator, AST):
    pass


class TypescriptTsxDecorator2(TypescriptTsxDecorator, AST):
    pass


class TypescriptTsxDefault(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDefaultType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxDelete(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDo(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxDoStatement(TypescriptTsxStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxElse(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxElseClause(TypescriptTsxAST, AST):
    pass


class TypescriptTsxEmptyStatement(TypescriptTsxStatement, AST):
    pass


class TypescriptTsxEnum(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxEnumAssignment(TypescriptTsxAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsxEnumBody(TypescriptTsxAST, AST):
    @_property
    def name(self) -> List[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxEnumBody0(TypescriptTsxEnumBody, AST):
    pass


class TypescriptTsxEnumBody1(TypescriptTsxEnumBody, AST):
    pass


class TypescriptTsxEnumBody2(TypescriptTsxEnumBody, AST):
    pass


class TypescriptTsxEnumBody3(TypescriptTsxEnumBody, AST):
    pass


class TypescriptTsxEnumBody4(TypescriptTsxEnumBody, AST):
    pass


class TypescriptTsxEnumDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore


class TypescriptTsxError(TypescriptTsxAST, ECMAError, ParseErrorAST, AST):
    pass


class TypescriptTsxErrorTree(ErrorTree, TypescriptTsxAST, AST):
    pass


class TypescriptTsxErrorVariationPoint(ErrorVariationPoint, TypescriptTsxAST, AST):
    @_property
    def parse_error_ast(self) -> Optional[AST]:
        return self.child_slot("parse_error_ast")  # type: ignore


class TypescriptTsxErrorVariationPointTree(ErrorVariationPoint, TypescriptTsxAST, AST):
    @_property
    def error_tree(self) -> Optional[AST]:
        return self.child_slot("error_tree")  # type: ignore


class TypescriptTsxEscapeSequence(TypescriptTsxAST, AST):
    pass


class TypescriptTsxExistentialType(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxExport(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxExportClause(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxExportClause0(TypescriptTsxExportClause, AST):
    pass


class TypescriptTsxExportClause1(TypescriptTsxExportClause, AST):
    pass


class TypescriptTsxExportClause2(TypescriptTsxExportClause, AST):
    pass


class TypescriptTsxExportClause3(TypescriptTsxExportClause, AST):
    pass


class TypescriptTsxExportSpecifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxExportStatement(TypescriptTsxStatement, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore

    @_property
    def decorator(self) -> List[AST]:
        return self.child_slot("decorator")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def declaration(self) -> Optional[AST]:
        return self.child_slot("declaration")  # type: ignore

    @_property
    def default(self) -> Optional[AST]:
        return self.child_slot("default")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxExportStatement0(TypescriptTsxExportStatement, AST):
    pass


class TypescriptTsxExportStatement1(TypescriptTsxExportStatement, AST):
    pass


class TypescriptTsxExportStatement2(TypescriptTsxExportStatement, AST):
    pass


class TypescriptTsxExpressionStatement(TypescriptTsxStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxExtends(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxExtendsClause(TypescriptTsxAST, AST):
    @_property
    def type_arguments(self) -> List[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def value(self) -> List[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxExtendsTypeClause(TypescriptTsxAST, AST):
    @_property
    def type(self) -> List[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxFalse(TypescriptTsxPrimaryExpression, BooleanFalseAST, AST):
    pass


class TypescriptTsxFinally(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxFinallyClause(TypescriptTsxAST, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxFlowMaybeType(TypescriptTsxPrimaryType, TypescriptFlowMaybeType, AST):
    pass


class TypescriptTsxFor(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxForInStatement(TypescriptTsxStatement, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore


class TypescriptTsxForInStatement0(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement1(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement2(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement3(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement4(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement5(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement6(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForInStatement7(TypescriptTsxForInStatement, AST):
    pass


class TypescriptTsxForStatement(TypescriptTsxStatement, AST):
    @_property
    def initializer(self) -> Optional[AST]:
        return self.child_slot("initializer")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def increment(self) -> Optional[AST]:
        return self.child_slot("increment")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxFormalParameters(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxFormalParameters0(TypescriptTsxFormalParameters, AST):
    pass


class TypescriptTsxFormalParameters1(TypescriptTsxFormalParameters, AST):
    pass


class TypescriptTsxFormalParameters2(TypescriptTsxFormalParameters, AST):
    pass


class TypescriptTsxFrom(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxFunction(TypescriptTsxPrimaryExpression, FunctionAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore


class TypescriptTsxFunctionDeclaration(TypescriptTsxDeclaration, TypescriptFunctionDeclaration, FunctionDeclarationAST, AST):
    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore


class TypescriptTsxFunctionSignature(TypescriptTsxDeclaration, TypescriptFunctionSignature, FunctionDeclarationAST, AST):
    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore


class TypescriptTsxFunctionSignature0(TypescriptTsxFunctionSignature, AST):
    pass


class TypescriptTsxFunctionSignature1(TypescriptTsxFunctionSignature, AST):
    pass


class TypescriptTsxFunctionTerminal(TypescriptTsxPrimaryExpression, FunctionAST, TerminalSymbol, AST):
    pass


class TypescriptTsxFunctionType(TypescriptTsxAST, AST):
    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore


class TypescriptTsxGeneratorFunction(TypescriptTsxPrimaryExpression, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxGeneratorFunctionDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore


class TypescriptTsxGenericType(TypescriptTsxPrimaryType, TypescriptGenericType, AST):
    pass


class TypescriptTsxGet(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxGlobal(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxHashBangLine(TypescriptTsxAST, AST):
    pass


class TypescriptTsxIdentifier(TypescriptTsxPattern, TypescriptTsxPrimaryExpression, TypescriptIdentifier, IdentifierAST, AST):
    pass


class TypescriptTsxIf(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxIfStatement(TypescriptTsxStatement, AST):
    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore


class TypescriptTsxIfStatement0(TypescriptTsxIfStatement, AST):
    pass


class TypescriptTsxIfStatement1(TypescriptTsxIfStatement, AST):
    pass


class TypescriptTsxImplements(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxImplementsClause(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxImport(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxImportAlias(TypescriptTsxDeclaration, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxImportClause(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxImportClause0(TypescriptTsxImportClause, AST):
    pass


class TypescriptTsxImportClause1(TypescriptTsxImportClause, AST):
    pass


class TypescriptTsxImportClause2(TypescriptTsxImportClause, AST):
    pass


class TypescriptTsxImportRequireClause(TypescriptTsxAST, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore


class TypescriptTsxImportSpecifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxImportStatement(TypescriptTsxStatement, AST):
    @_property
    def source(self) -> Optional[AST]:
        return self.child_slot("source")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxImportStatement0(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement1(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement2(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement3(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement4(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement5(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement6(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement7(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportStatement8(TypescriptTsxImportStatement, AST):
    pass


class TypescriptTsxImportTerminal(TypescriptTsxPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsxIn(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxIndexSignature(TypescriptIndexSignature, TypescriptTsxAST, AST):
    pass


class TypescriptTsxIndexSignature0(TypescriptTsxIndexSignature, AST):
    pass


class TypescriptTsxIndexSignature1(TypescriptTsxIndexSignature, AST):
    pass


class TypescriptTsxIndexSignature2(TypescriptTsxIndexSignature, AST):
    pass


class TypescriptTsxIndexSignature3(TypescriptTsxIndexSignature, AST):
    pass


class TypescriptTsxIndexTypeQuery(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxInfer(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxInferType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxInnerWhitespace(TypescriptTsxAST, InnerWhitespace, AST):
    pass


class TypescriptTsxInstanceof(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxInterface(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxInterfaceDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxInterfaceDeclaration0(TypescriptTsxInterfaceDeclaration, AST):
    pass


class TypescriptTsxInterfaceDeclaration1(TypescriptTsxInterfaceDeclaration, AST):
    pass


class TypescriptTsxInternalModule(TypescriptTsxExpression, TypescriptTsxDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxIntersectionType(TypescriptTsxPrimaryType, TypescriptIntersectionType, AST):
    pass


class TypescriptTsxIntersectionType0(TypescriptTsxIntersectionType, AST):
    pass


class TypescriptTsxIntersectionType1(TypescriptTsxIntersectionType, AST):
    pass


class TypescriptTsxIs(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxJsxAttribute(TypescriptTsxAST, AST):
    pass


class TypescriptTsxJsxAttribute0(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxAttribute1(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxAttribute2(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxAttribute3(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxAttribute4(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxAttribute5(TypescriptTsxJsxAttribute, AST):
    pass


class TypescriptTsxJsxClosingElement(TypescriptTsxAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxJsxElement(TypescriptTsxExpression, AST):
    @_property
    def open_tag(self) -> Optional[AST]:
        return self.child_slot("open_tag")  # type: ignore

    @_property
    def close_tag(self) -> Optional[AST]:
        return self.child_slot("close_tag")  # type: ignore


class TypescriptTsxJsxExpression(TypescriptTsxAST, AST):
    pass


class TypescriptTsxJsxExpression0(TypescriptTsxJsxExpression, AST):
    pass


class TypescriptTsxJsxExpression1(TypescriptTsxJsxExpression, AST):
    pass


class TypescriptTsxJsxFragment(TypescriptTsxExpression, AST):
    pass


class TypescriptTsxJsxNamespaceName(TypescriptTsxAST, AST):
    pass


class TypescriptTsxJsxOpeningElement(TypescriptTsxAST, AST):
    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxJsxOpeningElement0(TypescriptTsxJsxOpeningElement, AST):
    pass


class TypescriptTsxJsxOpeningElement1(TypescriptTsxJsxOpeningElement, AST):
    pass


class TypescriptTsxJsxSelfClosingElement(TypescriptTsxExpression, AST):
    @_property
    def attribute(self) -> List[AST]:
        return self.child_slot("attribute")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxJsxSelfClosingElement0(TypescriptTsxJsxSelfClosingElement, AST):
    pass


class TypescriptTsxJsxSelfClosingElement1(TypescriptTsxJsxSelfClosingElement, AST):
    pass


class TypescriptTsxJsxText(TypescriptTsxAST, AST):
    pass


class TypescriptTsxKeyof(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLabeledStatement(TypescriptTsxStatement, AST):
    @_property
    def label(self) -> Optional[AST]:
        return self.child_slot("label")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxLet(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLexicalDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def kind(self) -> Optional[AST]:
        return self.child_slot("kind")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxLiteralType(TypescriptTsxPrimaryType, TypescriptLiteralType, AST):
    pass


class TypescriptTsxLiteralType0(TypescriptTsxLiteralType, AST):
    pass


class TypescriptTsxLiteralType1(TypescriptTsxLiteralType, AST):
    pass


class TypescriptTsxLookupType(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxMappedTypeClause(TypescriptTsxAST, AST):
    @_property
    def alias(self) -> Optional[AST]:
        return self.child_slot("alias")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxMappedTypeClause0(TypescriptTsxMappedTypeClause, AST):
    pass


class TypescriptTsxMappedTypeClause1(TypescriptTsxMappedTypeClause, AST):
    pass


class TypescriptTsxMemberExpression(TypescriptTsxPattern, TypescriptTsxPrimaryExpression, ECMAMemberExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class TypescriptTsxMemberExpression0(TypescriptTsxMemberExpression, AST):
    pass


class TypescriptTsxMemberExpression1(TypescriptTsxMemberExpression, AST):
    pass


class TypescriptTsxMemberExpression2(TypescriptTsxMemberExpression, AST):
    pass


class TypescriptTsxMetaProperty(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxMethodDefinition(TypescriptTsxAST, AST):
    @_property
    def typescript_tsx_async(self) -> Optional[AST]:
        return self.child_slot("typescript_tsx_async")  # type: ignore

    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def getter_setter(self) -> Optional[AST]:
        return self.child_slot("getter_setter")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxMethodDefinition0(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition1(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition10(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition11(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition12(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition13(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition14(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition15(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition2(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition3(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition4(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition5(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition6(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition7(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition8(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodDefinition9(TypescriptTsxMethodDefinition, AST):
    pass


class TypescriptTsxMethodSignature(TypescriptTsxAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def getter_setter(self) -> Optional[AST]:
        return self.child_slot("getter_setter")  # type: ignore

    @_property
    def return_type(self) -> Optional[AST]:
        return self.child_slot("return_type")  # type: ignore

    @_property
    def parameters(self) -> Optional[AST]:
        return self.child_slot("parameters")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxMethodSignature0(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature1(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature10(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature100(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature101(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature102(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature103(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature104(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature105(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature106(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature107(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature108(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature109(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature11(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature110(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature111(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature112(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature113(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature114(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature115(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature116(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature117(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature118(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature119(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature12(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature120(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature121(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature122(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature123(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature124(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature125(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature126(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature127(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature13(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature14(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature15(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature16(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature17(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature18(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature19(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature2(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature20(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature21(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature22(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature23(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature24(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature25(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature26(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature27(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature28(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature29(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature3(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature30(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature31(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature32(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature33(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature34(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature35(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature36(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature37(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature38(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature39(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature4(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature40(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature41(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature42(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature43(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature44(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature45(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature46(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature47(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature48(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature49(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature5(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature50(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature51(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature52(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature53(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature54(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature55(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature56(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature57(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature58(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature59(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature6(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature60(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature61(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature62(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature63(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature64(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature65(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature66(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature67(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature68(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature69(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature7(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature70(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature71(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature72(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature73(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature74(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature75(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature76(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature77(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature78(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature79(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature8(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature80(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature81(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature82(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature83(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature84(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature85(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature86(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature87(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature88(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature89(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature9(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature90(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature91(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature92(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature93(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature94(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature95(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature96(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature97(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature98(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxMethodSignature99(TypescriptTsxMethodSignature, AST):
    pass


class TypescriptTsxModule(TypescriptTsxDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxModuleTerminal(TypescriptTsxDeclaration, TerminalSymbol, AST):
    pass


class TypescriptTsxNamedImports(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxNamedImports0(TypescriptTsxNamedImports, AST):
    pass


class TypescriptTsxNamedImports1(TypescriptTsxNamedImports, AST):
    pass


class TypescriptTsxNamedImports2(TypescriptTsxNamedImports, AST):
    pass


class TypescriptTsxNamedImports3(TypescriptTsxNamedImports, AST):
    pass


class TypescriptTsxNamespace(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNamespaceExport(TypescriptTsxAST, AST):
    pass


class TypescriptTsxNamespaceImport(TypescriptTsxAST, AST):
    pass


class TypescriptTsxNestedIdentifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxNestedTypeIdentifier(TypescriptTsxPrimaryType, AST):
    @_property
    def module(self) -> Optional[AST]:
        return self.child_slot("module")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxNever(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNew(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxNewExpression(TypescriptTsxExpression, AST):
    @_property
    def constructor(self) -> Optional[AST]:
        return self.child_slot("constructor")  # type: ignore

    @_property
    def type_arguments(self) -> Optional[AST]:
        return self.child_slot("type_arguments")  # type: ignore

    @_property
    def arguments(self) -> Optional[AST]:
        return self.child_slot("arguments")  # type: ignore


class TypescriptTsxNonNullExpression(TypescriptTsxPattern, TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxNull(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxNumber(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxObject(TypescriptTsxPrimaryExpression, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxObject0(TypescriptTsxObject, AST):
    pass


class TypescriptTsxObject1(TypescriptTsxObject, AST):
    pass


class TypescriptTsxObject2(TypescriptTsxObject, AST):
    pass


class TypescriptTsxObject3(TypescriptTsxObject, AST):
    pass


class TypescriptTsxObjectAssignmentPattern(TypescriptTsxAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore


class TypescriptTsxObjectPattern(TypescriptTsxPattern, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxObjectPattern0(TypescriptTsxObjectPattern, AST):
    pass


class TypescriptTsxObjectPattern1(TypescriptTsxObjectPattern, AST):
    pass


class TypescriptTsxObjectPattern2(TypescriptTsxObjectPattern, AST):
    pass


class TypescriptTsxObjectPattern3(TypescriptTsxObjectPattern, AST):
    pass


class TypescriptTsxObjectTerminal(TypescriptTsxPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsxObjectType(TypescriptTsxPrimaryType, TypescriptObjectType, AST):
    pass


class TypescriptTsxObjectType0(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType1(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType10(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType11(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType12(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType13(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType14(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType15(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType16(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType17(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType18(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType19(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType2(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType3(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType4(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType5(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType6(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType7(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType8(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxObjectType9(TypescriptTsxObjectType, AST):
    pass


class TypescriptTsxOf(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOmittingTypeAnnotation(TypescriptTsxAST, AST):
    pass


class TypescriptTsxOptingTypeAnnotation(TypescriptTsxAST, AST):
    pass


class TypescriptTsxOptionalParameter(TypescriptOptionalParameter, TypescriptParameter, ParameterAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxOptionalParameter0(TypescriptTsxOptionalParameter, AST):
    pass


class TypescriptTsxOptionalParameter1(TypescriptTsxOptionalParameter, AST):
    pass


class TypescriptTsxOptionalType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxOverride(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOverrideModifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxPair(TypescriptTsxAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsxPairPattern(TypescriptTsxAST, AST):
    @_property
    def key(self) -> Optional[AST]:
        return self.child_slot("key")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsxParenthesizedExpression(TypescriptTsxPrimaryExpression, AST):
    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsxParenthesizedExpression0(TypescriptTsxParenthesizedExpression, AST):
    pass


class TypescriptTsxParenthesizedExpression1(TypescriptTsxParenthesizedExpression, AST):
    pass


class TypescriptTsxParenthesizedType(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxPredefinedType(TypescriptTsxPrimaryType, TypescriptPredefinedType, AST):
    pass


class TypescriptTsxPrivate(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxPrivatePropertyIdentifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxProgram(TypescriptProgram, RootAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxProgram0(TypescriptTsxProgram, AST):
    pass


class TypescriptTsxProgram1(TypescriptTsxProgram, AST):
    pass


class TypescriptTsxPropertyIdentifier(TypescriptPropertyIdentifier, IdentifierAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxPropertySignature(TypescriptPropertySignature, TypescriptTsxAST, AST):
    pass


class TypescriptTsxPropertySignature0(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature1(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature10(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature11(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature12(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature13(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature14(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature15(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature2(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature3(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature4(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature5(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature6(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature7(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature8(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxPropertySignature9(TypescriptTsxPropertySignature, AST):
    pass


class TypescriptTsxProtected(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxPublic(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxPublicFieldDefinition(TypescriptTsxAST, AST):
    @_property
    def optional(self) -> Optional[AST]:
        return self.child_slot("optional")  # type: ignore

    @_property
    def modifiers(self) -> Optional[AST]:
        return self.child_slot("modifiers")  # type: ignore

    @_property
    def declare(self) -> Optional[AST]:
        return self.child_slot("declare")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore

    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore


class TypescriptTsxPublicFieldDefinition0(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition1(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition10(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition11(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition12(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition13(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition14(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition15(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition16(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition17(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition18(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition19(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition2(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition20(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition21(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition22(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition23(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition24(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition25(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition26(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition27(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition28(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition29(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition3(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition30(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition31(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition32(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition33(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition34(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition35(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition36(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition37(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition38(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition39(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition4(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition40(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition41(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition42(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition43(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition44(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition45(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition46(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition47(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition5(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition6(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition7(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition8(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxPublicFieldDefinition9(TypescriptTsxPublicFieldDefinition, AST):
    pass


class TypescriptTsxReadonly(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxReadonlyType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxRegex(TypescriptTsxPrimaryExpression, AST):
    @_property
    def pattern(self) -> Optional[AST]:
        return self.child_slot("pattern")  # type: ignore

    @_property
    def flags(self) -> Optional[AST]:
        return self.child_slot("flags")  # type: ignore


class TypescriptTsxRegexFlags(TypescriptTsxAST, AST):
    pass


class TypescriptTsxRegexPattern(TypescriptTsxAST, AST):
    pass


class TypescriptTsxRequire(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxRequiredParameter(TypescriptRequiredParameter, TypescriptParameter, ParameterAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxRequiredParameter0(TypescriptTsxRequiredParameter, AST):
    pass


class TypescriptTsxRequiredParameter1(TypescriptTsxRequiredParameter, AST):
    pass


class TypescriptTsxRestPattern(TypescriptTsxPattern, TypescriptRestPattern, ECMARestPattern, AST):
    pass


class TypescriptTsxRestPattern0(TypescriptTsxRestPattern, AST):
    pass


class TypescriptTsxRestPattern1(TypescriptTsxRestPattern, AST):
    pass


class TypescriptTsxRestPattern2(TypescriptTsxRestPattern, AST):
    pass


class TypescriptTsxRestPattern3(TypescriptTsxRestPattern, AST):
    pass


class TypescriptTsxRestType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxReturn(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxReturnStatement(TypescriptTsxStatement, ReturnAST, AST):
    pass


class TypescriptTsxReturnStatement0(TypescriptTsxReturnStatement, AST):
    pass


class TypescriptTsxReturnStatement1(TypescriptTsxReturnStatement, AST):
    pass


class TypescriptTsxSequenceExpression(TypescriptTsxAST, AST):
    @_property
    def left(self) -> Optional[AST]:
        return self.child_slot("left")  # type: ignore

    @_property
    def right(self) -> Optional[AST]:
        return self.child_slot("right")  # type: ignore

    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxSet(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxShorthandPropertyIdentifier(IdentifierAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxShorthandPropertyIdentifierPattern(IdentifierAST, TypescriptTsxAST, AST):
    pass


class TypescriptTsxSourceTextFragment(TypescriptTsxAST, SourceTextFragment, AST):
    pass


class TypescriptTsxSourceTextFragmentTree(ErrorTree, TypescriptTsxAST, AST):
    pass


class TypescriptTsxSourceTextFragmentVariationPoint(SourceTextFragmentVariationPoint, TypescriptTsxAST, AST):
    @_property
    def source_text_fragment(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment")  # type: ignore


class TypescriptTsxSourceTextFragmentVariationPointTree(SourceTextFragmentVariationPoint, TypescriptTsxAST, AST):
    @_property
    def source_text_fragment_tree(self) -> Optional[AST]:
        return self.child_slot("source_text_fragment_tree")  # type: ignore


class TypescriptTsxSpreadElement(TypescriptTsxAST, AST):
    pass


class TypescriptTsxStatementBlock(TypescriptTsxStatement, AST):
    pass


class TypescriptTsxStatementIdentifier(TypescriptTsxAST, AST):
    pass


class TypescriptTsxStatic(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxString(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxString0(TypescriptTsxString, AST):
    pass


class TypescriptTsxString1(TypescriptTsxString, AST):
    pass


class TypescriptTsxStringFragment(TypescriptTsxAST, AST):
    pass


class TypescriptTsxStringTerminal(TypescriptTsxPrimaryExpression, TerminalSymbol, AST):
    pass


class TypescriptTsxSubscriptExpression(TypescriptTsxPattern, TypescriptTsxPrimaryExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def index(self) -> Optional[AST]:
        return self.child_slot("index")  # type: ignore

    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore


class TypescriptTsxSubscriptExpression0(TypescriptTsxSubscriptExpression, AST):
    pass


class TypescriptTsxSubscriptExpression1(TypescriptTsxSubscriptExpression, AST):
    pass


class TypescriptTsxSuper(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxSwitch(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxSwitchBody(TypescriptTsxAST, AST):
    pass


class TypescriptTsxSwitchCase(TypescriptTsxAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxSwitchDefault(TypescriptTsxAST, AST):
    @_property
    def body(self) -> List[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxSwitchStatement(TypescriptTsxStatement, ControlFlowAST, AST):
    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxSymbol(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxTarget(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxTemplateLiteralType(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxTemplateString(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxTemplateSubstitution(TypescriptTsxAST, AST):
    pass


class TypescriptTsxTemplateType(TypescriptTsxAST, AST):
    pass


class TypescriptTsxTernaryExpression(TypescriptTsxExpression, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def consequence(self) -> Optional[AST]:
        return self.child_slot("consequence")  # type: ignore

    @_property
    def alternative(self) -> Optional[AST]:
        return self.child_slot("alternative")  # type: ignore


class TypescriptTsxThis(TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxThisType(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxThrow(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxThrowStatement(TypescriptTsxStatement, AST):
    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxTrue(TypescriptTsxPrimaryExpression, BooleanTrueAST, AST):
    pass


class TypescriptTsxTry(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxTryStatement(TypescriptTsxStatement, AST):
    @_property
    def finalizer(self) -> Optional[AST]:
        return self.child_slot("finalizer")  # type: ignore

    @_property
    def handler(self) -> Optional[AST]:
        return self.child_slot("handler")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxTryStatement0(TypescriptTsxTryStatement, AST):
    pass


class TypescriptTsxTryStatement1(TypescriptTsxTryStatement, AST):
    pass


class TypescriptTsxTryStatement2(TypescriptTsxTryStatement, AST):
    pass


class TypescriptTsxTryStatement3(TypescriptTsxTryStatement, AST):
    pass


class TypescriptTsxTupleType(TypescriptTsxPrimaryType, TypescriptTupleType, AST):
    pass


class TypescriptTsxTupleType0(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType1(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType2(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType3(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType4(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType5(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType6(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType7(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType8(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxTupleType9(TypescriptTsxTupleType, AST):
    pass


class TypescriptTsxType(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxTypeAliasDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type_parameters(self) -> Optional[AST]:
        return self.child_slot("type_parameters")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxTypeAnnotation(TypescriptTypeAnnotation, TypescriptTsxAST, AST):
    pass


class TypescriptTsxTypeArguments(TypescriptTypeArguments, TypescriptTsxAST, AST):
    pass


class TypescriptTsxTypeArguments0(TypescriptTsxTypeArguments, AST):
    pass


class TypescriptTsxTypeArguments1(TypescriptTsxTypeArguments, AST):
    pass


class TypescriptTsxTypeIdentifier(TypescriptTsxPrimaryType, TypeIdentifierAST, TypescriptTypeIdentifier, AST):
    pass


class TypescriptTsxTypeParameter(TypescriptTsxAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def constraint(self) -> Optional[AST]:
        return self.child_slot("constraint")  # type: ignore

    @_property
    def value(self) -> Optional[AST]:
        return self.child_slot("value")  # type: ignore


class TypescriptTsxTypeParameters(TypescriptTsxAST, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore


class TypescriptTsxTypeParameters0(TypescriptTsxTypeParameters, AST):
    pass


class TypescriptTsxTypeParameters1(TypescriptTsxTypeParameters, AST):
    pass


class TypescriptTsxTypePredicate(TypescriptTsxAST, AST):
    @_property
    def name(self) -> Optional[AST]:
        return self.child_slot("name")  # type: ignore

    @_property
    def type(self) -> Optional[AST]:
        return self.child_slot("type")  # type: ignore


class TypescriptTsxTypePredicateAnnotation(TypescriptTsxAST, AST):
    pass


class TypescriptTsxTypeQuery(TypescriptTsxPrimaryType, AST):
    pass


class TypescriptTsxTypeQuery0(TypescriptTsxTypeQuery, AST):
    pass


class TypescriptTsxTypeQuery1(TypescriptTsxTypeQuery, AST):
    pass


class TypescriptTsxTypeQuery2(TypescriptTsxTypeQuery, AST):
    pass


class TypescriptTsxTypeQuery3(TypescriptTsxTypeQuery, AST):
    pass


class TypescriptTsxTypeof(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxUnaryExpression(TypescriptTsxExpression, AST):
    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore

    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore


class TypescriptTsxUndefined(TypescriptTsxPattern, TypescriptTsxPrimaryExpression, AST):
    pass


class TypescriptTsxUnionType(TypescriptTsxPrimaryType, TypescriptUnionType, AST):
    pass


class TypescriptTsxUnionType0(TypescriptTsxUnionType, AST):
    pass


class TypescriptTsxUnionType1(TypescriptTsxUnionType, AST):
    pass


class TypescriptTsxUnknown(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxUpdateExpression(TypescriptTsxExpression, AssignmentAST, AST):
    @_property
    def argument(self) -> Optional[AST]:
        return self.child_slot("argument")  # type: ignore

    @_property
    def operator(self) -> Optional[AST]:
        return self.child_slot("operator")  # type: ignore


class TypescriptTsxUpdateExpression0(TypescriptTsxUpdateExpression, AST):
    pass


class TypescriptTsxUpdateExpression1(TypescriptTsxUpdateExpression, AST):
    pass


class TypescriptTsxVar(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxVariableDeclaration(TypescriptTsxDeclaration, AST):
    @_property
    def comma(self) -> List[AST]:
        return self.child_slot("comma")  # type: ignore

    @_property
    def semicolon(self) -> List[AST]:
        return self.child_slot("semicolon")  # type: ignore


class TypescriptTsxVariableDeclarator(TypescriptVariableDeclarator, ECMAVariableDeclarator, TypescriptTsxAST, AST):
    pass


class TypescriptTsxVariableDeclarator0(TypescriptTsxVariableDeclarator, AST):
    pass


class TypescriptTsxVariableDeclarator1(TypescriptTsxVariableDeclarator, AST):
    pass


class TypescriptTsxVoid(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxWhile(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxWhileStatement(TypescriptTsxStatement, ControlFlowAST, AST):
    @_property
    def condition(self) -> Optional[AST]:
        return self.child_slot("condition")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxWith(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxWithStatement(TypescriptTsxStatement, AST):
    @_property
    def object(self) -> Optional[AST]:
        return self.child_slot("object")  # type: ignore

    @_property
    def body(self) -> Optional[AST]:
        return self.child_slot("body")  # type: ignore


class TypescriptTsxYield(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxYieldExpression(TypescriptTsxExpression, AST):
    pass


class TypescriptTsxYieldExpression0(TypescriptTsxYieldExpression, AST):
    pass


class TypescriptTsxYieldExpression1(TypescriptTsxYieldExpression, AST):
    pass


class TypescriptTsxYieldExpression2(TypescriptTsxYieldExpression, AST):
    pass


class TypescriptTsxOpenBracket(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxCloseBracket(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseXor(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseXorAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBackQuote(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxOpenBrace(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxObjectTypeOpen(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseOr(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseOrAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLogicalOr(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxLogicalOrAssign(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxObjectTypeClose(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxCloseBrace(TypescriptTsxAST, TerminalSymbol, AST):
    pass


class TypescriptTsxBitwiseNot(TypescriptTsxAST, TerminalSymbol, AST):
    pass


