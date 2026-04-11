.PHONY: all primary supplementary verification calibration clean

all: primary supplementary

primary:
	python run_simulation.py --output-dir outputs/primary

supplementary: verification calibration

verification:
	python run_verification.py --output-dir outputs/verification

calibration:
	python run_calibration_sensitivity.py --output-dir outputs/calibration

clean:
	rm -rf outputs/
