import time
from oled_utils import oled_setup

oled = oled_setup()

# Test set 1
ppi_test_set_1 = [1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100, 1000, 1100]

# Test set 2
ppi_test_set_2 = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800]

while True:
    # Test set 1:
    
    # Mean PPI
    mean_ppi = sum(ppi_test_set_1) / len(ppi_test_set_1)

    # Mean HR
    mean_hr = int(60 / (mean_ppi / 1000))

    # Standard deviation of PPI
    diff = [(x - mean_ppi) ** 2 for x in ppi_test_set_1]
    var = sum(diff) / (len(ppi_test_set_1) - 1)
    sdnn = int(var ** 0.5)

    # Root mean square of successive differences
    diff = [ppi_test_set_1[i + 1] - ppi_test_set_1[i] for i in range(len(ppi_test_set_1) - 1)]
    sqr_diff = [diff ** 2 for diff in diff]
    m_sqr_diff = sum(sqr_diff) / len(sqr_diff)
    rmssd = int(m_sqr_diff ** 0.5)

    # Show test set 1 results on OLED screen for 5s
    oled.fill(0)
    oled.text("Test set 1:", 1, 1)
    oled.text(f"Mean PPI: {mean_ppi:.0f}ms", 1, 11)
    oled.text(f"Mean HR: {mean_hr}bpm", 1, 21)
    oled.text(f"sdnn: {sdnn}ms", 1, 31)
    oled.text(f"rmssd: {rmssd}ms", 1, 41)
    oled.show()

    time.sleep(5)


    # Test set 2:

    # Mean PPI
    mean_ppi = sum(ppi_test_set_2) / len(ppi_test_set_2)

    # Mean HR
    mean_hr = int(60 / (mean_ppi / 1000))

    # Standard deviation of PPI
    diff = [(x - mean_ppi) ** 2 for x in ppi_test_set_2]
    var = sum(diff) / (len(ppi_test_set_2) - 1)
    sdnn = int(var ** 0.5)

    # Root mean square of successive differences
    diff = [ppi_test_set_2[i + 1] - ppi_test_set_2[i] for i in range(len(ppi_test_set_2) - 1)]
    sqr_diff = [diff ** 2 for diff in diff]
    m_sqr_diff = sum(sqr_diff) / len(sqr_diff)
    rmssd = int(m_sqr_diff ** 0.5)

    # Show test set 2 results on OLED screen for 5s
    oled.fill(0)
    oled.text("Test set 2:", 1, 1)
    oled.text(f"Mean PPI: {mean_ppi:.0f}ms", 1, 11)
    oled.text(f"Mean HR: {mean_hr}bpm", 1, 21)
    oled.text(f"sdnn: {sdnn:.0f}ms", 1, 31)
    oled.text(f"rmssd: {rmssd:.0f}ms", 1, 41)
    oled.show()

    time.sleep(5)