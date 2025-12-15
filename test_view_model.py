"""
Quick test script for view_model measure.
"""
import os
import sys

# Ensure we can import the local toolkit source FIRST
sys.path.insert(0, os.path.abspath("src"))

import openstudio
from openstudio_toolkit.tasks.measures.create_view_model_html import run, validator


def test_view_model():
    """Test view_model measure with cabana-60 example."""

    print("=" * 60)
    print("🚀 Testing View Model Measure")
    print("=" * 60)

    # Load example model
    example_path = "examples/R2F-Office-Hub.osm"

    if not os.path.exists(example_path):
        print(f"❌ Model not found: {example_path}")
        return

    print(f"\n📂 Loading: {example_path}")

    translator = openstudio.osversion.VersionTranslator()
    model = translator.loadModel(example_path).get()

    print(f"✓ Model loaded")
    print(f"   Spaces: {len(model.getSpaces())}")
    print(f"   Surfaces: {len(model.getSurfaces())}")

    # Validate
    print("\n🔍 Running validator...")
    val = validator(model)
    print(f"Status: {val['status']}")

    if val['status'] != 'READY':
        print(f"❌ Validation failed: {val['messages']}")
        return

    # Run measure
    print("\n⚡ Running measure...")
    output = "test_report.html"

    try:
        result = run(model, output_path=output)

        if os.path.exists(result):
            size = os.path.getsize(result)
            print(f"\n✅ SUCCESS!")
            print(f"📊 Report: {result}")
            print(f"📏 Size: {size:,} bytes ({size/1024:.1f} KB)")
        else:
            print(f"❌ File not found: {result}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_view_model()
