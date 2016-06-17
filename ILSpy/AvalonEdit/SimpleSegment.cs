using ICSharpCode.AvalonEdit.Document;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Text;

namespace ICSharpCode.ILSpy.AvalonEdit
{
	/// <summary>
	/// Represents a simple segment (Offset,Length pair) that is not automatically updated
	/// on document changes.
	/// </summary>
	struct SimpleSegment : IEquatable<SimpleSegment>, ISegment
	{
		public static readonly SimpleSegment Invalid = new SimpleSegment(-1, -1);

		/// <summary>
		/// Gets the overlapping portion of the segments.
		/// Returns SimpleSegment.Invalid if the segments don't overlap.
		/// </summary>
		public static SimpleSegment GetOverlap(ISegment segment1, ISegment segment2)
		{
			int start = Math.Max(segment1.Offset, segment2.Offset);
			int end = Math.Min(segment1.EndOffset, segment2.EndOffset);
			if (end < start)
				return SimpleSegment.Invalid;
			else
				return new SimpleSegment(start, end - start);
		}

		public readonly int Offset, Length;

		int ISegment.Offset
		{
			get { return Offset; }
		}

		int ISegment.Length
		{
			get { return Length; }
		}

		public int EndOffset
		{
			get {
				return Offset + Length;
			}
		}

		public SimpleSegment(int offset, int length)
		{
			this.Offset = offset;
			this.Length = length;
		}

		public SimpleSegment(ISegment segment)
		{
			Debug.Assert(segment != null);
			this.Offset = segment.Offset;
			this.Length = segment.Length;
		}

		public override int GetHashCode()
		{
			unchecked {
				return Offset + 10301 * Length;
			}
		}

		public override bool Equals(object obj)
		{
			return (obj is SimpleSegment) && Equals((SimpleSegment)obj);
		}

		public bool Equals(SimpleSegment other)
		{
			return this.Offset == other.Offset && this.Length == other.Length;
		}

		public static bool operator ==(SimpleSegment left, SimpleSegment right)
		{
			return left.Equals(right);
		}

		public static bool operator !=(SimpleSegment left, SimpleSegment right)
		{
			return !left.Equals(right);
		}

		/// <inheritdoc/>
		public override string ToString()
		{
			return "[Offset=" + Offset.ToString(CultureInfo.InvariantCulture) + ", Length=" + Length.ToString(CultureInfo.InvariantCulture) + "]";
		}
	}

}
