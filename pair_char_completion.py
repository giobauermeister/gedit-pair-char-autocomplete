# -*- coding: utf-8 -*-
#
# Gedit plugin that does automatic pair character completion.
#
# Copyright © 2010, Kevin McGuinness <kevin.mcguinness@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
# 

__version__ = '1.0.0'
__author__ = 'Kevin McGuinness'

import gedit
import gtk

# Defaults
OPENING_PARENS = [ "(", "[", "{", "'", '"', '`' ]
CLOSING_PARENS = [ ")", "]", "}", "'", '"', '`' ]
DEFAULT_STMT_TERMINATOR = ';'
LANG_META_STMT_TERMINATOR_KEY = 'statement-terminator'
NEWLINE_CHAR = '\n'

def to_char(keyval_or_char):
  """Convert a event keyval or character to a character"""
  if isinstance(keyval_or_char, str):
    return keyval_or_char
  return chr(keyval_or_char) if 0 < keyval_or_char < 128 else None

class PairCompletionPlugin(gedit.Plugin):
  """Automatic pair character completion for gedit"""
  
  HandlerName = 'pair_char_completion_handler'
 
  def __init__(self):
    gedit.Plugin.__init__(self)
    self.ctrl_enter_enabled = True
 
  def activate(self, window):
    self.update_ui(window)
    
  def deactivate(self, window):
    for view in window.get_views():
      handler_id = getattr(view, self.HandlerName, None)
      if handler_id is not None:
        view.disconnect(handler_id)
      setattr(view, self.HandlerName, None)
    
  def update_ui(self, window):
    view = window.get_active_view()
    doc = window.get_active_document()
    if isinstance(view, gedit.View) and doc:
      if getattr(view, self.HandlerName, None) is None:
        handler_id = view.connect('key-press-event', self.on_key_press, doc)
        setattr(view, self.HandlerName, handler_id)
  
  def is_opening_paren(self,char):
    return char in OPENING_PARENS

  def is_closing_paren(self,char):
    return char in CLOSING_PARENS

  def get_matching_opening_paren(self,closer):
    try:
      return OPENING_PARENS[CLOSING_PARENS.index(closer)]
    except ValueError:
      return None

  def get_matching_closing_paren(self,opener):
    try:
      return CLOSING_PARENS[OPENING_PARENS.index(opener)]
    except ValueError:
      return None

  def would_balance_parens(self, doc, closing_paren):
    iter1 = doc.get_iter_at_mark(doc.get_insert())
    opening_paren = self.get_matching_opening_paren(closing_paren)
    balance = 1
    while balance != 0 and not iter1.is_start():
      iter1.backward_char()
      if iter1.get_char() == opening_paren:
        balance -= 1
      elif iter1.get_char() == closing_paren:
        balance += 1
    return balance == 0
  
  def compare_marks(self, doc, mark1, mark2):
    return doc.get_iter_at_mark(mark1).compare(doc.get_iter_at_mark(mark2))
  
  def enclose_selection(self, doc, opening_paren):
    closing_paren = self.get_matching_closing_paren(opening_paren)
    doc.begin_user_action()
    mark1 = doc.get_insert()
    mark2 = doc.get_selection_bound()
    if self.compare_marks(doc, mark1, mark2) > 0:
      mark1, mark2 = mark2, mark1
    doc.insert(doc.get_iter_at_mark(mark1), opening_paren)
    doc.insert(doc.get_iter_at_mark(mark2), closing_paren)
    iter1 = doc.get_iter_at_mark(mark2)
    doc.place_cursor(iter1)
    doc.end_user_action()
    return True
  
  def auto_close_paren(self, doc, opening_paren):
    closing_paren = self.get_matching_closing_paren(opening_paren)
    doc.begin_user_action()
    doc.insert_at_cursor(opening_paren+closing_paren)
    iter1 = doc.get_iter_at_mark(doc.get_insert())
    iter1.backward_char()
    doc.place_cursor(iter1)
    doc.end_user_action()
    return True
  
  def move_cursor_forward(self, doc):
    doc.begin_user_action()
    iter1 = doc.get_iter_at_mark(doc.get_insert())
    iter1.forward_char()
    doc.place_cursor(iter1)
    doc.end_user_action()
    return True

  def move_to_end_of_line_and_insert(self, doc, text):
    doc.begin_user_action()
    mark = doc.get_insert()
    iter1 = doc.get_iter_at_mark(mark)
    iter1.set_line_offset(0)
    iter1.forward_to_line_end()
    doc.place_cursor(iter1)
    doc.insert_at_cursor(text)
    doc.end_user_action()
    return True
    
  def get_char_under_cursor(self, doc):
    return doc.get_iter_at_mark(doc.get_insert()).get_char()
    
  def get_stmt_terminator(self, doc):
    terminator = DEFAULT_STMT_TERMINATOR
    lang = doc.get_language()
    if lang is not None:
      # Allow this to be changed by the language definition
      lang_terminator = lang.get_metadata(LANG_META_STMT_TERMINATOR_KEY) 
      if lang_terminator is not None:
        terminator = lang_terminator
    return terminator
  
  def get_current_line_indent(self, doc):
    it_start = doc.get_iter_at_mark(doc.get_insert())
    it_start.set_line_offset(0)
    it_end = it_start.copy()
    it_end.forward_to_line_end()
    indentation = []
    while it_start.compare(it_end) < 0:
      char = it_start.get_char()
      if char == ' ' or char == '\t':
        indentation.append(char)
      else:
        break
      it_start.forward_char()
    return ''.join(indentation)
  
  def is_ctrl_enter(self, event):
    return (self.ctrl_enter_enabled and 
      event.keyval == gtk.keysyms.Return and
      event.state & gtk.gdk.CONTROL_MASK)
  
  def should_auto_close_paren(self, doc):
    iter1 = doc.get_iter_at_mark(doc.get_insert())
    if iter1.is_end() or iter1.ends_line():
      return True
    char = iter1.get_char()
    return not (char.isalnum() or char == '_') 
  
  def on_key_press(self, view, event, doc):
    handled = False
    ch = to_char(event.keyval)
    if self.is_closing_paren(ch):
      # Skip over closing parenthesis if doing so would mean that the 
      # preceeding parenthesis are correctly balanced
      if (self.get_char_under_cursor(doc) == ch and 
          self.would_balance_parens(doc, ch)):
        handled = self.move_cursor_forward(doc)
    if not handled and self.is_opening_paren(ch):
      if doc.get_has_selection():
        # Enclose selection in parenthesis or quotes
        handled = self.enclose_selection(doc, ch)
      elif self.should_auto_close_paren(doc): 
        # Insert matching closing parenthesis and move cursor back one 
        handled = self.auto_close_paren(doc, ch)
    if not handled and self.is_ctrl_enter(event):
      # Handle Ctrl+Return and Ctrl+Shift+Return
      text_to_insert = NEWLINE_CHAR + self.get_current_line_indent(doc)
      if event.state & gtk.gdk.SHIFT_MASK:
        text_to_insert = self.get_stmt_terminator(doc) + text_to_insert
      self.move_to_end_of_line_and_insert(doc, text_to_insert)
      view.scroll_mark_onscreen(doc.get_insert())
      handled = True
    return handled

