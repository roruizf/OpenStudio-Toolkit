"""Integration test for the Hard Size HVAC measure."""

from pathlib import Path

from openstudio_toolkit.tasks.measures import hard_size_hvac
from openstudio_toolkit.utils.osm_utils import load_osm_file_as_model


def test_hard_size_hvac(tmp_path: Path) -> None:
    model_path = Path(__file__).parent / "resources" / "small_office.osm"
    assert model_path.exists()

    model = load_osm_file_as_model(str(model_path))
    model.getWeatherFile().remove()
    result_osm_path = tmp_path / "test_hard_size_hvac_result.osm"

    result_model = hard_size_hvac.run(osm_model=model, output_path=str(result_osm_path))

    assert result_model is not None
    assert result_osm_path.exists()
