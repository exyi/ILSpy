using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Media;
using ICSharpCode.AvalonEdit.Document;
using ICSharpCode.AvalonEdit.Rendering;
using Mono.Cecil;

namespace ICSharpCode.ILSpy.TextView
{
	public class SemanticCodeHighlighter : DocumentColorizingTransformer
	{
		#region colors
		public static readonly Brush ClassReferenceColor = new SolidColorBrush(Color.FromRgb(78, 201, 176));
		public static readonly Brush InterfaceReferenceColor = new SolidColorBrush(Color.FromRgb(184, 215, 163));
		public static readonly Brush KeywordColor = new SolidColorBrush(Color.FromRgb(86, 156, 204));
		public static readonly Brush CommentColor = new SolidColorBrush(Color.FromRgb(96, 139, 78));
		public static readonly Brush StringLiteralColor = new SolidColorBrush(Color.FromRgb(214, 157, 133));
		#endregion


		private TextSegmentCollection<ReferenceSegment> references;
		private TextSegmentCollection<HighlightedSegment> specials;

		public void ClearSegments()
		{
			references = null;
			specials = null;
		}

		public void SetSegments(AvalonEditTextOutput text)
		{
			references = text.References;
			specials = text.HighlightedSegments;
		}

		protected override void ColorizeLine(DocumentLine line)
		{
			if (references != null) {
				foreach (var reference in references.FindOverlappingSegments(line)) {
					HighlightSegment(reference);
				}
			}
			if (specials != null) {
				foreach (var segment in specials.FindOverlappingSegments(line)) {
					HighlightSegment(segment);
				}
			}
		}

		void HighlightSegment(HighlightedSegment segment)
		{
			Brush brush = null;
			var bold = false;
			switch (segment.Type) {
				case Decompiler.SpecialSegmentType.None:
					break;
				case Decompiler.SpecialSegmentType.DocComment:
					break;
				case Decompiler.SpecialSegmentType.Comment:
					brush = CommentColor;
					break;
				case Decompiler.SpecialSegmentType.Keyword:
					brush = KeywordColor;
					break;
				case Decompiler.SpecialSegmentType.StringLiteral:
					brush = StringLiteralColor;
					break;
				case Decompiler.SpecialSegmentType.NumberLiteral:
					brush = StringLiteralColor;
					break;
				default:
					break;
			}
			if (bold || brush != null) ChangeLinePart(segment.StartOffset, segment.EndOffset, vle => SetElementColor(vle, brush, bold));
		}

		void HighlightSegment(ReferenceSegment reference)
		{
			var bold = reference.IsLocalTarget && !reference.IsLocal;

			Brush brush = null;
			if (reference.Reference is TypeReference) {
				var typeDefinition = ((TypeReference)reference.Reference).Resolve();
				if (typeDefinition != null) {
					if (typeDefinition.IsInterface || typeDefinition.IsEnum) brush = InterfaceReferenceColor;
					else brush = ClassReferenceColor;
				}
			}

			if (bold || brush != null) ChangeLinePart(reference.StartOffset, reference.EndOffset, vle => SetElementColor(vle, brush, bold));
		}

		void SetElementColor(VisualLineElement element, Brush brush, bool bold = false)
		{
			if (brush != null) element.TextRunProperties.SetForegroundBrush(brush);
			if (bold) element.TextRunProperties.SetTypeface(new Typeface(
				 element.TextRunProperties.Typeface.FontFamily,
				 element.TextRunProperties.Typeface.Style,
				 System.Windows.FontWeights.Bold,
				 element.TextRunProperties.Typeface.Stretch));
		}
	}
}
