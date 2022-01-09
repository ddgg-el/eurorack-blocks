##############################################################################
#
#     visitor.py
#     Copyright (c) 2020 Raphael DINGE
#
#Tab=3########################################################################



import os
from .arpeggio import PTNodeVisitor
from . import ast
from . import adapter
from . import grammar



class Visitor (PTNodeVisitor):

   def __init__ (self, parser, **kwargs):
      super (Visitor, self).__init__ (defaults=True, **kwargs)
      self.parser = parser
      self.filename = None

   def set_filename (self, filename):
      self.filename = filename

   def to_identifier (self, node):
      return adapter.Identifier (self.parser, node)

   def to_keyword (self, node):
      return adapter.Keyword (self.parser, node)

   def to_symbol (self, node):
      return adapter.Symbol (self.parser, node)

   def to_literal (self, node):
      return adapter.Literal (self.parser, node)


   #-- Names -----------------------------------------------------------------

   def visit_identifier  (self, node, children):
      return self.to_identifier (node)

   def visit_name  (self, node, children):
      return self.visit_identifier (node, children)


   #-- Literals --------------------------------------------------------------

   def visit_string_literal (self, node, children):
      return ast.StringLiteral (self.to_literal (node))


   #-- Module ----------------------------------------------------------------

   def visit_module_declaration (self, node, children):
      global_namespace = ast.GlobalNamespace ()

      module_identifier = children.module_name [0]

      module = ast.Module (module_identifier)
      global_namespace.add (module)

      if children.module_body:
         entities = children.module_body [0]
         module.add (entities)

      return global_namespace

   def visit_module_name (self, node, children):
      return self.visit_identifier (node, children)

   def visit_module_body (self, node, children):
      return children [0] if children else []

   def visit_module_entities (self, node, children):
      return list (children)


   #-- Library ---------------------------------------------------------------

   def visit_library_declaration (self, node, children):
      library = ast.Library ()

      if children.module_entities:
         entities = children.module_entities [0]
         library.add (entities)

      return library


   #-- File ------------------------------------------------------------------

   def visit_file_declaration (self, node, children):
      string_literal = children.string_literal [0]
      dir_name = os.path.dirname (self.filename)
      file_path = os.path.join (dir_name, string_literal.value)
      file_path_str = str (file_path)
      file = ast.File (file_path_str, string_literal)

      return file


   #-- Import ----------------------------------------------------------------

   def visit_import_declaration (self, node, children):
      string_literal = children.string_literal [0]
      dir_name = os.path.dirname (self.filename)
      file_path = os.path.join (dir_name, string_literal.value)
      file_path_str = str (file_path)
      import_ = ast.Import (file_path_str, string_literal)

      return import_


   #-- Define ----------------------------------------------------------------

   def visit_define_declaration (self, node, children):
      define_key_identifier = children.define_key [0]
      define_value = children.define_value [0]

      define = ast.Define (define_key_identifier, define_value)

      return define

   def visit_define_key (self, node, children):
      return self.visit_identifier (node, children)

   def visit_define_value (self, node, children):
      return self.to_literal (node)


   #-- Sources ---------------------------------------------------------------

   def visit_sources_declaration (self, node, children):

      sources = ast.Sources ()

      if children.sources_body:
         entities = children.sources_body [0]
         sources.add (entities)

      return sources

   def visit_sources_body (self, node, children):
      return children [0] if children else []

   def visit_sources_entities (self, node, children):
      return list (children)


   #-- Base ------------------------------------------------------------------

   def visit_base_declaration (self, node, children):
      string_literal = children.string_literal [0]
      dir_name = os.path.dirname (self.filename)
      file_path = os.path.join (dir_name, string_literal.value)
      file_path_str = str (file_path)
      base = ast.Base (file_path_str, string_literal)

      return base
