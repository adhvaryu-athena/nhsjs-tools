---
student_name: "Aaryamann Goenka"
manuscript_title: "Do Global Forest Datasets Accurately Map Mangroves in Mumbai?"
reviewer_decision_date: "2026-02-04"
target_submit_date: "2026-03-01"
voice_overrides: []
references_added: []
---

## P1
OP: FIND_REPLACE
FIND: "Mangroves are essential specialised trees that provide carbon storage, shoreline stabilization, and natural flood protection, especially in densely populated cities like Mumbai. However, reported estimates of mangrove extent show differences depending on the datasets and classification methods used. The purpose of this study is to evaluate the differences between Hansen Global Forest Change(GFC) and Global Mangrove Watch(GMW), so that it can be determined whether these datasets accurately represent mangroves in Mumbai. This analysis was limited to the 20N 070E region which includes Mumbai’s mangroves. The methodology began by reprojecting the dataset images to EPSG:32643 coordinate system, with GMW being used as the baseline mangrove mask. Within this mask, Hansen’s first and last year of detection data were analyzed to assess spatial agreement, and persistence. Results show that 92% of GMW mangroves were detected as forest at least once in GFC; however, no pixels were classified as persistent forest and rather only temporary forest, with pixels having a median detection duration near zero years. This result is scientifically suspicious and suggests the unstable forest signals within mangrove regions likely caused by tidal effects, phenology, or canopy structure. These findings suggest that Hansen can detect mangroves, but with unstable short lasting signals. Datasets such as GMW, which incorporate radar data and greater coastal parameters, are more suitable for extent mapping and for identifying mangrove zones."
REPLACE: "Mangroves are specialised trees that provide significant carbon storage. They also play a crucial role in shoreline stabilization and natural flood protection, especially in densely populated cities like Mumbai. However, reported estimates of mangrove extent show differences depending on the datasets and classification methods used. The purpose of this study is to evaluate the differences between Hansen Global Forest Change(GFC) and Global Mangrove Watch(GMW), so that it can be determined whether these datasets accurately represent mangroves in Mumbai. This analysis was limited to the Hansen 20N 070E tile and the merged GMW tiles N20E072 and N20E073, covering Mumbai's mangroves and the adjacent Thane Creek system. The methodology began by reprojecting the dataset images to EPSG:32643 coordinate system, with GMW being used as the reference mangrove mask. Within this mask, Hansen's treecover2000, lossyear, and gain layers were used to assess spatial agreement and forest stability. Results show that approximately 17.5% of GMW pixels are classified as persistent forest in Hansen and 82.5% as never forest, with detected loss within the mangrove mask effectively absent (14 pixels, ≈0.07 ha). This pattern suggests Hansen captures the dense interior mangrove canopy but misses the majority of GMW pixels along sparse fringes and narrow tidal channels, likely due to the 10% canopy threshold combined with optical-sensing limitations in intertidal environments. These findings suggest that Hansen and GMW disagree systematically under this workflow, though without field validation this disagreement cannot be read as evidence that either product is more accurate. Datasets such as GMW, which incorporate radar data and greater coastal parameters, may provide more direct coverage for extent mapping and for identifying mangrove zones."

## P2
OP: FIND_REPLACE
FIND: "Mangroves are specialised trees and shrubs that grow in saline water in intertidal zones. They are characterized by: high carbon dioxide retention capabilities, strong, stilt-like roots that help them survive in muddy and changing water levels, making them one of the most essential coastal ecosystems around the world. "
REPLACE: "Mangroves are specialised trees and shrubs that grow in saline water in intertidal zones. They have high carbon dioxide retention capabilities as well as strong, stilt-like roots that help them survive in muddy and changing water levels, making them one of the most important coastal habitats around the world."

## P3
OP: FIND_REPLACE
FIND: "They are extremely effective carbon sinks, storing around 1000 tonnes of carbon per hectare, far greater than terrestrial forests. Moreover, they act as natural coastal defenders against various climate events and calamities1. In fact, a 100 meter belt of mangroves can reduce wave height by 13-66% through their dense root network’s ability to dissipate wave energy and trap sediments protecting against storm surges and flood risks2. Apart from this, they aid in trapping sediments, which stabilize shorelines and reduce erosion. "
REPLACE: " Moreover, they act as natural coastal defenders against various climate events and calamities[[CITE:2]]. In fact, a 100 meter belt of mangroves can reduce wave height by 13-66% through their dense root network's ability to dissipate wave energy and trap sediments. This buffering effect protects against storm surges and flood risks[[CITE:3]]. Apart from this, they aid in trapping sediments, which stabilize shorelines and reduce erosion."

## P4
OP: FIND_REPLACE
FIND: "For densely populated coastal cities such as Mumbai, these features are extremely critical- their functions are approximately valued at ₹1700 crore annually, and the Thane creek mangrove belt alone stores around 238,000 tonnes of carbon3,4. Apart from the ecological aspects, these mangroves also protect fishing communities' livelihoods, by promoting biodiversity and providing nursing grounds for fish and other marine life5. Overall, all the aforementioned functions of mangroves make them indispensable for the environment, especially in the case of Mumbai itself. "
REPLACE: "For densely populated coastal cities such as Mumbai, these features are extremely critical- their functions are approximately valued at ₹1700 crore annually as reported by the Maharashtra Mangrove and Marine Biodiversity Conservation Foundation, with peer-reviewed studies further documenting the ecosystem-service value of Mumbai's mangroves[[CITE:4]], and the Thane Creek mangrove belt has been measured at average above- and below-ground carbon densities of approximately 117–128 Mg C ha-1 [[CITE:5]]. Apart from the ecological aspects, these mangroves also protect fishing communities' livelihoods, by promoting biodiversity and providing nursing grounds for fish and other marine life[[CITE:6]]. Overall, all the aforementioned functions of mangroves make them indispensable for the environment, especially in the case of Mumbai itself."

## P5
OP: FIND_REPLACE
FIND: "Mumbai, one of India’s most densely populated cities contains one of the largest urban mangrove covers in the world. These are spread all around the periphery of Mumbai, with the majority of mangroves being concentrated in Thane creek, Mahim, Versova, and Gorai8. The reported total cover varies due to varying mapping methods, but recent studies show Greater Mumbai’s mangrove cover is around 50-70km2, while the Mumbai suburban district contributes around 64km2 of mangroves6. The Thane Creek Sanctuary is the largest protected mangrove region in the area, with a reported site area of around 65km2 according to one source, and 90km2 according to another. This disagreement may be an effect of how boundaries are defined (such as the inclusion/disclusion of areas enclosed within mangroves)6."
REPLACE: "Mumbai, one of India's most densely populated cities contains one of the largest urban mangrove covers in the world. These are spread all around the periphery of Mumbai, with the majority of mangroves being concentrated in Thane creek, Mahim, Versova, and Gorai[[CITE:7]]. The reported total cover varies due to varying mapping methods, but recent studies show Greater Mumbai's mangrove cover is around 50-70km[[CITE:2]], while the Mumbai suburban district contributes around 64km[[CITE:2]] of mangroves[[CITE:8]]. The Thane Creek Sanctuary is the largest protected mangrove region in the area, with a reported site area of around 65km[[CITE:2]] according to one source, and 90km[[CITE:2]] according to another. This disagreement may be an effect of how boundaries are defined (such as the inclusion/disclusion of areas enclosed within mangroves)[[CITE:8]]."

## P6
OP: FIND_REPLACE
FIND: "However, despite their importance, Mumbai’s mangroves have faced continuous threats of destruction, fragmentation, or thinning from many different angles. Due to the rapid urbanization persistent in Mumbai, projects such as the coastal road, other industrial development projects, and even illegal encroachment, mangrove loss and fragmentation have been inevitably proliferating. Moreover, recurring issues as a result of weak regulatory enforcement including untreated sewage discharge and illegal waste dumping have degraded the water and land where mangroves usually thrive, hence posing a threat to their health. Rapid climate change, sea level rise, and increased frequency of extreme rainfall, alter the habitat of mangroves irreparably, further worsening this crisis. "
REPLACE: "However, despite their importance, Mumbai's mangroves have faced continuous threats of destruction, fragmentation, or thinning from many different angles. Due to the rapid urbanization persistent in Mumbai, projects such as the coastal road, other industrial development projects, and even illegal encroachment, mangrove loss and fragmentation have been inevitably proliferating. Moreover, recurring issues as a result of weak regulatory enforcement including untreated sewage discharge and illegal waste dumping have degraded the water and land where mangroves usually thrive, hence posing a threat to their health. Rapid climate change, sea level rise, and increased frequency of extreme rainfall, alter the habitat of mangroves irreparably, further worsening this crisis."

## P7
OP: FIND_REPLACE
FIND: "Numerous studies have attempted to quantify the exact changes of mangrove cover in Mumbai, but most have varying results based on spatial extent, time frame, as well as resolution of imaging. Some studies which employ satellite imagery (Landsat or Sentinel data) have reported local increases or even doubling of mangrove cover in parts of Thane Creek from 79.14km2 in 1990 to 154.5km2 in 2017 attributed to the deposition of sediment that has allowed mangroves to spread closer to the center of the creek7,8. In contrast, some other studies report marginal declines or near stability in total mangrove cover over multiple decades, with the total mangrove area in Mumbai being 50.52km2 in 2004, and 48.7km2 in 20139. These contrasting findings are likely not only due to differing scales at which the change is analyzed, which may capture local regional expansion instead of net regional change, but rather the datasets and classification methods employed. "
REPLACE: "Numerous studies have attempted to quantify the exact changes of mangrove cover in Mumbai, but most have varying results based on spatial extent, time frame, as well as resolution of imaging. Some studies which employ satellite imagery (Landsat or Sentinel data) have reported local increases or even doubling of mangrove cover in parts of Thane Creek from 79.14km[[CITE:2]] in 1990 to 154.5km[[CITE:2]] in 2017 attributed to the deposition of sediment that has allowed mangroves to spread closer to the center of the creek[[CITE:7,9]]. In contrast, some other studies report marginal declines or near stability in total mangrove cover over multiple decades, with the total mangrove area in Mumbai being 50.52km[[CITE:2]] in 2004, and 48.7km[[CITE:2]] in 2013[[CITE:10]]. More recent satellite-based assessments using machine-learning classifiers and high-resolution imagery have continued to refine these estimates[[CITE:11,12]]. These contrasting findings are likely not only due to differing scales at which the change is analyzed, which may capture local regional expansion instead of net regional change, but rather the datasets and classification methods employed."

## P8
OP: FIND_REPLACE
FIND: "This study focuses on a comparison of mangrove datasets in Mumbai using two major global datasets: Hansen Global Forest Change (GFC) and Global Mangrove Watch (GMW). The scope of this paper is limited to evaluating spatial agreement, temporal detection behavior, and classification stability of areas within Mumbai’s coastal regions. Additionally, the research does not attempt to quantify actual area loss, or to model future scenarios, but rather focuses on how dataset choice can influence interpretation of both extent and persistence in these surrounding regions. "
REPLACE: "This study focuses on a comparison of mangrove datasets in Mumbai using two major global datasets: Hansen Global Forest Change (GFC) and Global Mangrove Watch (GMW). The scope of this paper is limited to evaluating spatial agreement, temporal detection behavior, and classification stability of areas within Mumbai's coastal regions. Additionally, the research does not attempt to quantify actual area loss, or to model future scenarios, but rather focuses on how dataset choice can influence interpretation of both extent and persistence in these surrounding regions."

## P9
OP: FIND_REPLACE
FIND: "One potential limitation of this study is that it’s constrained to Mumbai and its surrounding coastal mangrove ecosystems. When selecting the co-ordinates for the analysis we used: (20N 070E - Hansen, 20N 070E- GMW), which covered the majority of mangroves found surrounding Mumbai’s urban area. Hence, due to the small area being considered in this study, the findings provide meaningful insights into datasets within this coastal context, however they can’t be directly generalized to other regions with mangroves globally, due to differing canopy structures, sediment characteristics, tidal cycles or climatic conditions. Moreover, Mumbai itself is a unique coastal ecosystem considering its one of the only metropolitan cities surrounded by mangroves. Therefore, its ecology would differ as compared to other such ecosystems."
REPLACE: "One potential limitation of this study is that it's constrained to Mumbai and its surrounding coastal mangrove areas. When selecting the co-ordinates for the analysis we used: the Hansen 20N 070E tile and the merged GMW tiles N20E072 and N20E073, which covered the majority of mangroves found surrounding Mumbai's urban area and Thane Creek. Some mangroves near the very edges of these tiles may fall outside the aligned analysis grid, which is noted as a minor scope limitation. Hence, due to the small area being considered in this study, the findings provide meaningful insights into datasets within this coastal context; however, they cannot be directly generalized to other mangrove systems globally, due to differences in canopy structure, sediment characteristics, tidal cycles, or climate. Moreover, Mumbai itself is a unique coastal ecosystem considering its one of the only metropolitan cities surrounded by mangroves. Therefore, its ecology would differ as compared to other such systems."

## P10
OP: FIND_REPLACE
FIND: "Additionally, the comparative analysis is only limited to two widely used datasets: Hansen Global Forest Change (GFC) and Global Mangrove Watch (GMW). Although these are among the most commonly referenced datasets for most use cases due to their multi-dataset integration methodology, other high-resolution or region-specific datasets were not included in this paper such as ESA World cover10, or the Jaxa ALOS PALSAR dataset11. As a result, the conclusions only reflect discrepancies and consistencies between these two datasets, which don’t span all available mangrove or forest monitoring datasets."
REPLACE: "Additionally, the comparative analysis is only limited to two widely used datasets: Hansen Global Forest Change (GFC) and Global Mangrove Watch (GMW). Although these are among the most commonly referenced datasets for most use cases because they combine multiple satellite data sources, other high-resolution or region-specific datasets were not included in this paper such as ESA World cover[[CITE:13]], or the Jaxa ALOS PALSAR dataset[[CITE:14]]. As a result, the conclusions only reflect agreement and disagreement between these two datasets, which don't span all available mangrove or forest monitoring datasets."

## P11
OP: FIND_REPLACE
FIND: "The study is focused on the mangrove ecosystems within the Mumbai region in India. The analysis was restricted to the tile corresponding to 20N, 70E in the Hansen dataset. This tile encompasses the majority of the mangrove cover surrounding Mumbai, including Thane Creek, Mahim, Versova, and Gorai. All spatial analyses were conducted at pixel level within this defined region."
REPLACE: "The study is focused on the mangrove ecosystems within the Mumbai region in India. The analysis was restricted to the tile corresponding to 20N, 70E in the Hansen dataset, with the mangrove mask defined from the corresponding GMW tiles (N20E072 and N20E073, merged). This tile encompasses the majority of the mangrove cover surrounding Mumbai, including Thane Creek, Mahim, Versova, and Gorai. All spatial analyses were conducted at pixel level within this defined region."

## P12
OP: FIND_REPLACE
FIND: "GFC is a general forest temporal dataset derived mainly from Landsat optical imagery with a 30m resolution, which maps tree cover and annual loss/gain using canopy cover and height thresholds12. Since it doesn't explicitly separate mangroves from other first or wetland vegetation, it is more susceptible to the effects of cloud cover, mixed coastal pixels, and flooding, leading to the omission or misclassification of mangroves. "
REPLACE: "The Hansen Global Forest Change (GFC) product is a general forest temporal dataset derived mainly from Landsat optical imagery with a 30m resolution, which maps tree cover and annual loss/gain using canopy cover and height thresholds[[CITE:15]]. Since it doesn't explicitly separate mangroves from other forest or wetland vegetation, it is more susceptible to the effects of cloud cover, mixed coastal pixels, and flooding, leading to the omission or misclassification of mangroves."

## P13
OP: FIND_REPLACE
FIND: "In this dataset, forest is taken as vegetation with more than 10% canopy cover. The following layers appear within the dataset: "
REPLACE: "In this dataset, forest is defined as vegetation with more than 10% canopy cover. The GFC layers used in this study are: tree cover baseline (treecover2000), which records the percentage canopy cover for each pixel as of the year 2000; loss year (lossyear), which encodes the calendar year a pixel transitioned from forest to non-forest as integers from 1 (corresponding to 2001) through 24 (corresponding to 2024), with 0 meaning no detected loss; and forest gain (gain), a binary flag marking pixels classified as gaining forest cover between 2000 and 2012. The first and last reflectance composite bands provided in the GFC product were not used for temporal analysis in this study, since these contain Landsat reflectance values rather than annual forest state."

## P14
OP: DELETE_RANGE
START_PARAGRAPH_STARTS_WITH: "Tree cover baseline (treecover2000)"
END_PARAGRAPH_STARTS_WITH: "Last year of forest detection"

## P15
OP: FIND_REPLACE
FIND: "The GMW dataset gives spatially explicit binary classification of mangrove extent. GMW is a mangrove-specific spatial dataset that integrates radar data (ALOS PALSAR) with optical imagery and coastal habitat masks, allowing it to more accurately detect mangroves in waterlogged, intertidal environments13. Due to their unique techniques of collecting data, including differences in sensor type (only optical vs radar+optical), classification thresholds, spatial resolution, and ecological constraints, there are often discrepancies between the two. "
REPLACE: "The GMW dataset gives spatially explicit binary classification of mangrove extent. GMW is a mangrove-specific spatial dataset that integrates radar data (ALOS PALSAR) with optical imagery and coastal habitat masks, allowing it to more accurately detect mangroves in waterlogged, intertidal environments[[CITE:16]]. The Global Mangrove Watch v3 dataset (2020 epoch) was used in this study[[CITE:17]]; the two tiles N20E072 and N20E073 were merged before analysis to cover the full Mumbai coastline and Thane Creek system. GMW itself is not free of error: published validations note omission and commission errors of narrow or fragmented mangrove patches, increased uncertainty in disturbed or intertidal regions, and artefacts introduced by sensor limitations, which can lead to under- or over-counting of mangrove pixels in some regions[[CITE:17,18]]. Due to their unique techniques of collecting data, including differences in sensor type (only optical vs radar+optical), classification thresholds, spatial resolution, and ecological constraints, there are often discrepancies between the two."

## P16
OP: FIND_REPLACE
FIND: "In this study, the GMW was the baseline mask used to define the spatial extent within which all other detection analysis was performed. Unlike GMW, the Hansen dataset does not distinguish mangroves from other forest types. It detects tree cover based on spectral classification and canopy thresholds. "
REPLACE: "In this study, the GMW was the reference mask used to define the spatial extent within which all other detection analysis was performed, not as a validated ground truth. Unlike GMW, the Hansen dataset does not distinguish mangroves from other forest types. It detects tree cover based on spectral classification and canopy thresholds."

## P17
OP: FIND_REPLACE
FIND: "All raster preprocessing was performed using Python, primarily with the rasterio, numpy, and pyproj libraries14, 15, 16, 17."
REPLACE: "All raster preprocessing was performed using Python, primarily with the rasterio, numpy, and pyproj libraries[[CITE:19,20,21,22]]. The Hansen GFC analysis covers the period from 2000 to 2024, set by the treecover2000 baseline and the 2024 release of the lossyear band."

## P18
OP: FIND_REPLACE
FIND: "Then the pixel area was calculated for both datasets using the relation: Pixel area (m²) = |pixel width × pixel height|. Which leads to area, in hectares, as Area (ha) = (pixel count × pixel area in m²) / 10,000. All statistics in the Results section come from this calculation.  "
REPLACE: "Then the pixel area was calculated for both datasets using the relation: Pixel area (m[[CITE:2]]) = |pixel width × pixel height|. Which leads to area, in hectares, as Area (ha) = (pixel count × pixel area in m[[CITE:2]]) / 10,000. All statistics in the Results section come from this calculation."

## P19
OP: FIND_REPLACE
FIND: "A mask, that selected where mangroves were detected, was created for GFC and two values extracted: First year of forest detection and Last year of forest detection. These values encode the first and last years in which Hansen classified the pixel as forest. From this we created three classifications: Never forest, Temporary forest & Persistent forest. Basically, where pixels were never detected as mangroves, where they were for some years but not all and where they were always detected. This classification allowed assessment of forest stability within mangrove areas. From this forest detection duration was calculated as the difference between last year and first year of detection. A histogram of detection duration was generated to evaluate persistence patterns, and a spatial duration map was created to identify geographic clustering of stable versus unstable forest detection."
REPLACE: "Nodata pixels in treecover2000 and lossyear were treated as zero after masking to the GMW extent. Pixels where the GMW mask was zero or nodata were excluded from all calculations."

## P20
OP: FIND_REPLACE
FIND: "To quantify agreement between datasets, the following spatial comparisons were computed:"
REPLACE: "A mask was created from the merged GMW tiles to restrict all analysis to mangrove pixels. Within this mask, three pixel classes were derived from the GFC layers. Pixels with treecover2000 below 10% and gain equal to 0 were classified as never forest. Pixels with treecover2000 at or above 10% and lossyear equal to 0 were classified as persistent forest, since they were forested in 2000 with no detected loss. Pixels with treecover2000 at or above 10% and lossyear greater than 0, or where gain equalled 1 and lossyear was greater than 0, were classified as temporary forest. Basically, never forest captures pixels that Hansen never read as canopy, persistent forest captures stable canopy across the record, and temporary forest captures pixels with detected loss at some point."

## P21
OP: FIND_REPLACE
FIND: "Mangrove pixels detected as forest in Hansen"
REPLACE: "In compact form:never forest := treecover2000 < 10 AND gain == 0persistent forest := treecover2000 ≥ 10 AND lossyear == 0temporary forest := (treecover2000 ≥ 10 AND lossyear > 0) OR (gain == 1 AND lossyear > 0)"

## P22
OP: FIND_REPLACE
FIND: "Mangrove pixels not detected as forest in Hansen"
REPLACE: "For temporary forest pixels, the calendar year of forest loss was recovered by adding 2000 to the lossyear value (so a lossyear of 8 corresponds to 2008). The distribution of these decoded years was used to assess when within the 2001–2024 record forest loss was detected within the GMW mask."

## P23
OP: FIND_REPLACE
FIND: "Hansen forest pixels outside GMW mangrove areas"
REPLACE: "To quantify agreement between datasets, three spatial comparisons were computed: the count of mangrove pixels inside GMW that Hansen also classified as forest, the count of mangrove pixels inside GMW that Hansen did not classify as forest, and the count of Hansen forest pixels falling outside GMW mangrove areas. These are summarized both visually and numerically in the Results section."

## P24
OP: DELETE_PARAGRAPH
PARAGRAPH_STARTS_WITH: "These are summarized both visually and numerically in the Results section."

## P25
OP: FIND_REPLACE
FIND: "After reprojection and grid alignment to the Hansen 30m resolution grid (EPSG:32643), the total mangrove area within the study region was calculated as 1508.85 hectares based on the Global Mangrove Watch (GMW) mask. All subsequent forest detection analysis was restricted to these mangrove-classified pixels."
REPLACE: "After reprojection and grid alignment to the Hansen 30m resolution grid (EPSG:32643), the total mangrove area within the study region was calculated as approximately 12,852 hectares (ha) based on the merged Global Mangrove Watch (GMW) mask. This figure exceeds Mumbai-specific mangrove cover estimates of 50–70 km[[CITE:2]] cited in some sources because the merged GMW tiles also include adjacent mangrove systems along Thane Creek and the broader Konkan coastline within the analysis region. All subsequent forest detection analysis was restricted to these mangrove-classified pixels."

## P26
OP: FIND_REPLACE
FIND: "These results show that the total GMW mangrove area in the study region is approximately 1508.85 ha, with around 92% of mangrove areas having at least one year of forest detection in Hansen, while about 8% never show a forest signal. Furthermore, the spatial visualizations show clear areas where Hansen detects forest outside GMW mangroves and vice-versa. Put together, these findings suggest that Hansen can generally detect mangroves, but not without flaws in detection potentially caused by sparse canopies, young/degraded mangroves, tidal flooding, and sensor limitation (low resolution)."
REPLACE: "These results show that the total GMW mangrove area in the study region is approximately 12,852 ha, with approximately 17.5% (2,251.96 ha) of GMW pixels classified as persistent forest by Hansen and 82.5% (10,600.34 ha) classified as never forest. Detected forest loss within the mangrove mask was effectively absent, with only 14 pixels (≈0.07 ha) classified as temporary forest. Furthermore, the spatial visualizations show clear areas where Hansen detects forest outside GMW mangroves and vice-versa. Put together, these findings suggest that Hansen detects a stable persistent core within the GMW mask but consistently misses the majority of GMW-classified pixels, particularly along sparse fringe and edge areas. The disagreement is consistent with the limitations of optical sensing in intertidal environments."

## P27
OP: FIND_REPLACE
FIND: "For each mangrove pixel, the first and last years of Hansen forest detection were extracted. The spatial distribution of first detection years shows earlier forest signals concentrated in inland mangrove regions, while later detections are more spatially fragmented. The last detection map reveals patchy and discontinuous forest signals across mangrove areas, suggesting instability in classification over time."
REPLACE: "Table 2. Area breakdown of agreement between Hansen GFC and GMW within the analysis region."

## P28
OP: FIND_REPLACE
FIND: "Figure 2. Spatial distribution of first and last year of Hansen forest detection within GMW mangroves. Two maps showing (top) the first year and (bottom) the last year that Hansen classifies a pixel as forest, restricted to pixels inside the GMW mangrove mask. Values are decoded to calendar years using the encoding described in Methods. Spatial patterns indicate where forest detection appears earlier versus later, and where forest detection persists longer into the record."
REPLACE: "The Hansen-only area covers the entire 10°×10° tile and largely reflects non-mangrove forest cover across the broader Konkan and Western Ghats region; it is reported here for completeness but is not directly comparable to the GMW mangrove extent."

## P29
OP: FIND_REPLACE
FIND: "Histograms of first and last detection years further demonstrate that forest detection does not occur uniformly across the mangrove system."
REPLACE: "In terms of the classification of mangroves within the GMW mask, results show approximately 2,251.96 ha (17.5%) of pixels are classified as persistent forest by Hansen — pixels that crossed the 10% canopy cover threshold in 2000 and showed no detected loss through 2024. Approximately 10,600.34 ha (82.5%) are classified as never forest, meaning Hansen's treecover2000 layer never registered them as forest under the 10% canopy threshold and no gain was recorded. The median canopy cover within the GMW mask is 0% and the mean is 3.27%, with 82.5% of pixels falling below the 10% threshold (Figure 2), confirming that the disagreement is driven by the threshold itself rather than by sensor instability over time."

## P30
OP: FIND_REPLACE
FIND: "Figure 3. Histograms of first-year and last-year Hansen forest detections within GMW mangroves. Distributions of (top) first detection year and (bottom) last detection year for mangrove pixels with valid detections. These histograms summarize whether forest detection begins and ends uniformly across the mangrove system or is concentrated in specific time ranges. Bin counts represent pixel counts on the aligned grid."
REPLACE: "Figure 2. Distribution of Hansen treecover2000 values within the GMW mangrove mask. Histogram of canopy cover percentage for all 172,727 GMW pixels (5%-wide bins). The dashed red line marks Hansen's 10% forest threshold. 82.5% of pixels fall below the threshold (mean = 3.27%, median = 0%), with the remaining 17.5% spread across canopy cover values from 10% to ≈30%. Pixels above the threshold correspond to the persistent-forest class shown in Figure 3."

## P31
OP: FIND_REPLACE
FIND: "In terms of the classification of mangroves, results show approximately 1393.22 ha (92.34%) of mangroves are classified as “temporary forest” in the Hansen dataset based on the first > 0 and last<latest criterion (Forest signals appear at some point but disappear before the latest year). On the other hand, approximately 115.63 ha (7.66%) are classified as “never forest” (first == 0) in the Hansen dataset. "
REPLACE: "Temporary forest pixels are essentially absent in the dataset: only 14 pixels (≈0.07 ha) within the entire GMW mask have a detected loss event between 2001 and 2024. As a category, temporary forest contributes negligibly to the analysis (under 0.001%) and is best read as scattered noise at 30 m resolution rather than as evidence of meaningful mangrove loss."

## P32
OP: FIND_REPLACE
FIND: "However, persistent forest (first>0 and last==latest) is found to be 0 ha, conveying that all persistent forest pixels are being classified as temporary forest. This outcome is extremely suspicious considering that mangroves have long lifespans and don’t simply remain in a constant cycle of dying out as the data is suggesting."
REPLACE: "Together, these results suggest that Hansen detects a stable persistent core of mangrove canopy within the densest creek clusters, while systematically missing the majority of GMW-classified pixels. The class map (Figure 3) and a zoom into the southern Mumbai cluster (Figure 4) show that never-forest pixels are concentrated along creek edges, narrow tidal channels, and sparse outer-fringe areas where canopy density is below the 10% threshold, rather than in dense mangrove cores. This pattern is consistent with the optical-sensing limitations described earlier, not with widespread mangrove loss."

## P33
OP: FIND_REPLACE
FIND: "Due to the suspicious and unstable nature of these results, this data doesn’t imply that mangroves are disappearing, but rather suggests that Hansen’s forest classification is unstable when applied to Mumbai’s mangrove ecosystems. "
REPLACE: "Figure 3. Mangrove forest presence classes derived from Hansen GFC layers within the GMW mangrove mask. Categorical map classifying GMW pixels into: never forest (treecover2000 below 10% with no gain recorded), persistent forest (treecover2000 ≥ 10% with no detected loss through 2024), and temporary forest (treecover2000 ≥ 10% with a detected loss year, or gain followed by loss). Class definitions follow the criteria stated in Methods."

## P34
OP: FIND_REPLACE
FIND: "Figure 4. Mangrove forest presence classes derived from Hansen first/last detection (within the GMW mask). Categorical map classifying GMW mangrove pixels into: never forest (no Hansen detection), temporary forest (detected at least once but not present through the latest year), and persistent forest (detected and still present in the latest year). Class definitions follow the first/last criteria stated in Methods and are applied only inside the GMW mangrove extent. "
REPLACE: "Figure 4. Spatial pattern of never-forest and persistent-forest pixels within a southern Mumbai mangrove cluster. Zoom on the central Mahim–Versova system and the adjacent eastern peninsular patch (EPSG:32643, eastings 265–290 km, northings 2,110–2,140 km). Persistent forest (dark green; treecover2000 ≥ 10% with no detected loss) clusters in dense interior patches, while never-forest (gray; treecover2000 < 10%) wraps fringes, narrow tidal channels, and outer-island edges. Class definitions follow the criteria in Methods. Temporary forest is not visible at this scale (14 pixels in total across the full GMW mask)."

## P35
OP: FIND_REPLACE
FIND: "The duration analysis discussed in the methodology section showed: "
REPLACE: "The temporal distribution of the few detected loss events is shown in Figure 5. Of the 14 loss pixels, 5 (36%) have a recorded loss year in 2003–2008 and 9 (64%) in 2023–2024; the median loss year is 2008. Given the small absolute count, this distribution is best interpreted as scattered noise rather than systematic forest loss within the GMW mask."

## P36
OP: FIND_REPLACE
FIND: "A median duration near zero years"
REPLACE: "Figure 5. Distribution of Hansen-detected forest loss years within the GMW mangrove mask, 2001–2024. Histogram includes only the 14 GMW pixels (≈0.07 ha) where Hansen recorded a loss-year value. A small cluster of pixels falls in 2003–2008 and the remainder in 2023–2024."

## P37
OP: FIND_REPLACE
FIND: "A distribution dominated by short detection intervals"
REPLACE: "These results indicate that Hansen's forest classification is internally consistent across the GMW mask — pixels above the canopy threshold remain classified through 2024 — but the threshold itself excludes the majority of pixels GMW identifies as mangrove. The disagreement between the two products therefore reflects a difference in detection sensitivity rather than temporal instability of the forest signal."

## P38
OP: DELETE_RANGE
START_PARAGRAPH_STARTS_WITH: "Numerous pixels exhibiting near-zero or minimal persistence"
END_PARAGRAPH_STARTS_WITH: "The duration spatial map further indicates that mangrove pixels aren’t persistent in the Hansen dataset and regularly flicker in and out of its classification of forest. Apart from the reasons stated"

## P39
OP: FIND_REPLACE
FIND: "Although over 92% of mangrove pixels exhibit forest detection at least once, the near absence of persistent forest classification suggests that Hansen’s forest definition does not consistently capture mangrove ecosystems over time."
REPLACE: "Although approximately 17.5% of mangrove pixels are classified as persistent forest in Hansen, the 82.5% that are not classified as forest at all suggests that Hansen's forest definition does not consistently capture mangrove ecosystems under its 10% canopy threshold."

## P40
OP: FIND_REPLACE
FIND: "This instability appears to reflect classification variability rather than large-scale mangrove loss, as cumulative loss within the mangrove mask was minimal over the study period."
REPLACE: "This disagreement appears to reflect a difference in detection sensitivity rather than large-scale mangrove loss, as cumulative loss within the mangrove mask was minimal over the study period."

## P41
OP: FIND_REPLACE
FIND: "Several factors can plausibly explain why mangrove pixels may flicker in and out of Hansen’s forest classification:"
REPLACE: "Several factors can plausibly explain why Hansen misses the majority of GMW-classified pixels."

## P42
OP: FIND_REPLACE
FIND: "First, mangroves occur in intertidal zones where the observed surface reflectance changes substantially with the tidal stage. Even if vegetation is unchanged, the mixture of water, mudflat, and canopy within a pixel can vary across images, causing unstable classification at 30 m resolution."
REPLACE: "Mangroves occur in intertidal zones where the observed surface reflectance changes substantially with the tidal stage[[CITE:23]]. Even if vegetation is unchanged, the mixture of water, mudflat, and canopy within a pixel can vary across images, causing unstable classification at 30 m resolution."

## P43
OP: FIND_REPLACE
FIND: "Second, mangrove canopy structure is often heterogeneous and can be sparse or low in height compared to many inland forests. Pixels with canopy cover near a fixed threshold (e.g., 10%) may move above or below the detection boundary due to seasonal effects, partial inundation, atmospheric conditions, or mixed-pixel effects."
REPLACE: "Additionally, mangrove canopy structure is often heterogeneous and can be sparse or low in height compared to many inland forests. Pixels with canopy cover near a fixed threshold (e.g., 10%) may move above or below the detection boundary due to seasonal effects, partial inundation, atmospheric conditions, or mixed-pixel effects[[CITE:24]]."

## P44
OP: FIND_REPLACE
FIND: "Third, optical imagery is sensitive to cloud cover and haze, which can reduce usable observations and increase uncertainty in coastal regions. Radar-based inputs in GMW are less affected by cloud cover and can better discriminate against vegetated surfaces in wet environments, contributing to higher classification stability."
REPLACE: "Moreover, optical imagery is sensitive to cloud cover and haze, which can reduce usable observations and increase uncertainty in coastal regions. Radar-based inputs in GMW are less affected by cloud cover and can better discriminate against vegetated surfaces in wet environments, contributing to higher classification stability[[CITE:25,26]]."

## P45
OP: FIND_REPLACE
FIND: "These factors jointly suggest that Hansen’s “forest persistence” signal may reflect classification variability as much as ecological change when applied to mangroves."
REPLACE: "These factors jointly suggest that Hansen's forest detection signal may reflect canopy threshold sensitivity as much as ecological structure when applied to mangroves."

## P46
OP: FIND_REPLACE
FIND: "A critical interpretation point is that “temporary forest” in this analysis does not necessarily represent real ecological loss of mangroves. Instead, it indicates that Hansen does not detect forest consistently at that pixel across time. Therefore, the observed dominance of temporary classifications should be interpreted as a limitation of applying a general forest product to a coastal wetland ecosystem, not as evidence that Mumbai’s mangroves are repeatedly disappearing and returning."
REPLACE: "A critical interpretation point is that 'never forest' in this analysis does not necessarily represent the absence of mangroves. Instead, it indicates that Hansen does not detect canopy at that pixel under its 10% threshold. Therefore, the observed dominance of never-forest classifications should be interpreted as a limitation of applying a general forest product to coastal wetland vegetation, not as evidence that mangroves are absent from these areas."

## P47
OP: FIND_REPLACE
FIND: "This distinction is important because Hansen products are frequently used in environmental monitoring workflows and policy discussions. If mangroves are frequently mischaracterized as non-persistent forest, conclusions about mangrove degradation or stability derived from Hansen alone may be biased."
REPLACE: "This distinction is important because Hansen products are frequently used in environmental monitoring workflows and policy discussions. If mangroves are frequently mischaracterized as non-forest, conclusions about mangrove extent or change derived from Hansen alone may be biased."

## P48
OP: FIND_REPLACE
FIND: "Mangroves are increasingly treated as natural infrastructure due to their role in coastal protection and flood risk reduction. For cities such as Mumbai, mangrove mapping supports environmental impact assessment, coastal regulation compliance, and resilience planning. The results here imply that dataset choice can strongly influence interpretation of mangrove persistence and change."
REPLACE: "Mangroves are increasingly treated as natural infrastructure due to their role in coastal protection and flood risk reduction. For cities such as Mumbai, mangrove mapping supports environmental impact assessment, coastal regulation compliance, and resilience planning. The results here imply that dataset choice can strongly influence interpretation of mangrove extent and change."

## P49
OP: FIND_REPLACE
FIND: "Specifically, Hansen-derived forest stability metrics may underrepresent mangrove persistence in intertidal environments and may not be appropriate as a standalone tool for monitoring mangrove stability. GMW-style mangrove-specific products, which incorporate radar and coastal constraints, are likely more suitable for baseline extent mapping and for identifying mangrove zones for planning purposes."
REPLACE: "Specifically, Hansen-derived forest detection metrics may underrepresent mangrove extent in intertidal environments . However, since this study does not include field validation, the disagreement between the two products under this workflow does not establish that one is more accurate than the other. GMW-style mangrove-specific products, which incorporate radar and coastal constraints, may be better suited to baseline extent mapping and for identifying mangrove zones for planning purposes."

## P50
OP: FIND_REPLACE
FIND: "First, it focuses on a single geographic region (Mumbai) and a limited spatial tile. Results may not directly generalize to mangroves with different canopy structures, sediment regimes, tidal ranges, or climatic conditions."
REPLACE: "It focuses on a single geographic region (Mumbai) and a limited spatial tile. Results may not directly generalize to mangroves with different canopy structures, sediment regimes, tidal ranges, or climatic conditions."

## P51
OP: FIND_REPLACE
FIND: "Second, this analysis compares only two widely used datasets. Additional datasets (e.g., ESA WorldCover mangrove classes or regionally validated mangrove maps) could provide further context."
REPLACE: "This analysis compares only two widely used datasets. Additional datasets (e.g., ESA WorldCover mangrove classes or regionally validated mangrove maps) could provide further context."

## P52
OP: FIND_REPLACE
FIND: "Third, interpretation depends on correct decoding of Hansen temporal layers (first/last year). While the workflow standardizes projections and aligns grids for fair comparison, temporal encoding and nodata conventions require careful handling. Any remaining ambiguity in first/last encoding would affect persistence and duration estimates."
REPLACE: "The comparison framework also has a temporal mismatch: GMW v3 represents a single 2020 epoch baseline, while the Hansen analysis covers 2000–2024 through the treecover2000 baseline and the lossyear band. The two products are therefore being compared across different temporal references, and the persistence findings should be read with this design constraint in mind."

## P53
OP: FIND_REPLACE
FIND: "Finally, this study does not include field validation. Instead, it focuses on internal consistency and comparative behavior between datasets."
REPLACE: "Finally, this study does not include field validation. Instead, it focuses on internal consistency and comparative behavior between datasets. These results should therefore be read as a caution about dataset choice, rather than a comprehensive accountof mangrove change in Mumbai."

## P54
OP: FIND_REPLACE
FIND: "Overall, the results suggest that Hansen Global Forest Change can detect mangrove vegetation in Mumbai intermittently, but does not provide stable forest persistence signals within mangrove environments. The disagreement between Hansen and GMW is systematic and likely driven by sensor modality differences, intertidal mixed-pixel effects, and threshold-based classification limitations. These findings support the broader conclusion that ecosystem-specific datasets are necessary for reliable mangrove monitoring and that applying generic forest persistence metrics to mangroves requires caution."
REPLACE: "Overall, the results suggest that Hansen Global Forest Change detects a stable persistent core of canopy within Mumbai's mangroves but misses the majority of GMW-classified pixels under its 10% canopy threshold. The disagreement between Hansen and GMW is systematic and likely driven by sensor modality differences, intertidal mixed-pixel effects, and threshold-based classification limitations. Since this study does not include field validation, these findings show product disagreement under the workflow used here rather than relative accuracy of either product. They nonetheless suggest that mangrove monitoring should account for the design assumptions of any single-source forest dataset."

## P55
OP: FIND_REPLACE
FIND: "I would like to thank my mentor for guidance on project design, methodology, and paper editing. I also thank the developers and maintainers of the Global Mangrove Watch and Hansen Global Forest Change datasets for making their data publicly available. This work used open-source Python tools including Rasterio, NumPy, Pandas, Matplotlib, and related geospatial libraries for data processing and visualization."
REPLACE: "I would like to thank the project supervisors for guidance on project design, methodology, and paper editing. I also thank the developers and maintainers of the Global Mangrove Watch and Hansen Global Forest Change datasets for making their data publicly available. This work used open-source Python tools including Rasterio, NumPy, Pandas, Matplotlib, and related geospatial libraries for data processing and visualization."

## P56
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "References"
INSERT: "D. C. Donato, J. B. Kauffman, D. Murdiyarso, S. Kurnianto, M. Stidham, M. Kanninen. Mangroves among the most carbon-rich forests in the tropics. Nature Geoscience. Vol. 4, pg. 293–297, 2011, https://doi.org/10.1038/ngeo1123."

## P57
OP: FIND_REPLACE
FIND: "V. Chandrashekhar. Mumbai residents show “will to pay” for mangrove conservation. https://timesofindia.indiatimes.com/india/mumbai-residents-show-will-to-pay-for-mangrove-conservation/articleshow/119779108.cms, 2025."
REPLACE: "M. Everard, R. R. S. Jha, S. Russell. The benefits of fringing mangrove systems to Mumbai. Aquatic Conservation: Marine and Freshwater Ecosystems. Vol. 24, pg. 256–274, 2014, https://doi.org/10.1002/aqc.2433."

## P58
OP: FIND_REPLACE
FIND: "S. Rebello. Mumbai: Thane mangroves act as carbon sink. https://www.hindustantimes.com/mumbai/mumbai-thane-mangroves-act-as-carbon-sink/story-s5r3st85ustmlXt0LvWS6M.html, 2015."
REPLACE: "S. G. Singh, A. Vennila, R. Singh, V. S. Bharti, S. P. Shukla, C. S. Purushothaman. Standing carbon stock of Thane Creek mangrove ecosystem: An integrated approach using allometry and remote sensing techniques. Regional Studies in Marine Science. Vol. 67, pg. 103207, 2023, https://doi.org/10.1016/j.rsma.2023.103207."

## P59
OP: FIND_REPLACE
FIND: "Food and Agriculture Organization of the United Nations. The world’s mangroves 1980–2005. https://www.fao.org/4/a1427e/a1427e00.htm, 2007."
REPLACE: "Food and Agriculture Organization of the United Nations. The world's mangroves 1980–2005. https://www.fao.org/4/a1427e/a1427e00.htm, 2007."

## P60
OP: FIND_REPLACE
FIND: "Ministry of Environment, Forest and Climate Change (MoEFCC). Forest survey of India: State of forest report 2017. https://www.gktoday.in/state-of-the-forest-report-2017/, 2017."
REPLACE: "NASA Earth Observatory. Monitoring Mumbai's mangroves. https://science.nasa.gov/earth/earth-observatory/monitoring-mumbais-mangroves-91333/, 2017."

## P61
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "NASA Earth Observatory. Monitoring Mumbai's mangroves. https://science.nasa.gov/earth/earth-observatory/monitoring-mumbais-mangroves-91333/, 2017."
INSERT: "Forest Survey of India. India state of forest report 2017 — mangrove cover chapter. Ministry of Environment, Forest and Climate Change, Government of India, Dehradun, 2018, https://fsi.nic.in/isfr2017/isfr-mangrove-cover-2017.pdf."

## P62
OP: FIND_REPLACE
FIND: "NASA Earth Observatory. Monitoring Mumbai’s mangroves. https://science.nasa.gov/earth/earth-observatory/monitoring-mumbais-mangroves-91333/, 2017."
REPLACE: "A. Abhyankar, T. Sahoo, B. Seth, P. Mohapatra, S. Palai, P. Bhargava, S. Chaurasiya, S. Isasare. Mapping and change detection of mangroves around Mumbai using remote sensing and geographic information systems (GIS). Journal of Civil Engineering, Science and Technology. Vol. 12, 2021, https://doi.org/10.33736/jcest.3339.2021."

## P63
OP: FIND_REPLACE
FIND: "A. Abhyankar, T. Sahoo, B. Seth, P. Mohapatra, S. Palai, P. Bhargava, S. Chaurasiya, S. Isasare. Mapping and change detection of mangroves around Mumbai using remote sensing and geographic information systems (GIS). Journal of Civil Engineering, Science and Technology. Vol. 12, 2021, https://www.researchgate.net/publication/356756294_MAPPING_AND_CHANGE_DETECTION_OF_MANGROVES_AROUND_MUMBAI_USING_REMOTE_SENSING_AND_GEOGRAPHIC_INFORMATION_SYSTEMS_GIS."
REPLACE: "S. Sawant, P. Bonala, A. Joshi, M. Shindikar, A. Patil, S. Vyas, D. Deobagkar. Integration of machine learning and remote sensing for assessing the change detection of mangrove forests along the Mumbai coast. Journal of Earth System Science. Vol. 133, pg. 237, 2024, https://doi.org/10.1007/s12040-024-02378-0."

## P64
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "and remote sensing for assessing the change detection of mangrove forests along the Mumbai coast. Journal of Earth System Science. Vol. 133, pg. 237, 2024, https://doi.org/10.1007/s12040-024-02378-0."
INSERT: "P. Nagarajan, L. Rajendran, N. D. Pillai, G. Lakshmanan. Comparison of machine learning algorithms for mangrove species identification in Malad creek, Mumbai using WorldView-2 and Google Earth images. Journal of Coastal Conservation. Vol. 26, pg. 44, 2022, https://doi.org/10.1007/s11852-022-00891-2."

## P65
OP: FIND_REPLACE
FIND: "M. C. Hansen, P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, J. R. G. Townshend. High-resolution global maps of 21st-century forest cover change. Science. Vol. 342, pg. 850-853, 2013, https://doi.org/10.1126/science.1244693."
REPLACE: "M. C. Hansen, P. V. Potapov, R. Moore, M. Hancher, S. A. Turubanova, A. Tyukavina, D. Thau, S. V. Stehman, S. J. Goetz, T. R. Loveland, A. Kommareddy, A. Egorov, L. Chini, C. O. Justice, J. R. G. Townshend. High-resolution global maps of 21st-century forest cover change. Science. Vol. 342, pg. 850–853, 2013, https://doi.org/10.1126/science.1244693."

## P66
OP: FIND_REPLACE
FIND: "P. Bunting, A. Rosenqvist, R. M. Lucas, L. M. Rebelo, L. Hilarides, N. Thomas, A. Hardy, T. Itoh, M. Shimada, C. M. Finlayson. The global mangrove watch - A new 2010 global baseline of mangrove extent. Remote Sensing. Vol. 10, pg. 1669, 2018, https://doi.org/10.3390/rs10101669."
REPLACE: "P. Bunting, A. Rosenqvist, R. M. Lucas, L. M. Rebelo, L. Hilarides, N. Thomas, A. Hardy, T. Itoh, M. Shimada, C. M. Finlayson. The global mangrove watch — A new 2010 global baseline of mangrove extent. Remote Sensing. Vol. 10, pg. 1669, 2018, https://doi.org/10.3390/rs10101669."

## P67
OP: FIND_REPLACE
FIND: "C. R. Harris, K. J. Millman, S. J. van der Walt, et al. Array programming with NumPy. Nature. Vol. 585, pg. 357–362, 2020, https://doi.org/10.1038/s41586-020-2649-2."
REPLACE: "P. Bunting, A. Rosenqvist, L. Hilarides, R. M. Lucas, N. Thomas, T. Tadono, T. A. Worthington, M. Spalding, N. J. Murray, L.-M. Rebelo. Global mangrove extent change 1996–2020: Global Mangrove Watch Version 3.0. Remote Sensing. Vol. 14, pg. 3657, 2022, https://doi.org/10.3390/rs14153657."

## P68
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "ngton, M. Spalding, N. J. Murray, L.-M. Rebelo. Global mangrove extent change 1996–2020: Global Mangrove Watch Version 3.0. Remote Sensing. Vol. 14, pg. 3657, 2022, https://doi.org/10.3390/rs14153657."
INSERT: "P. Bunting, A. Rosenqvist, L. Hilarides, R. M. Lucas, N. Thomas. Global Mangrove Watch: Updated 2010 mangrove forest extent (v2.5). Remote Sensing. Vol. 14, pg. 1034, 2022, https://doi.org/10.3390/rs14041034."

## P69
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "ng, A. Rosenqvist, L. Hilarides, R. M. Lucas, N. Thomas. Global Mangrove Watch: Updated 2010 mangrove forest extent (v2.5). Remote Sensing. Vol. 14, pg. 1034, 2022, https://doi.org/10.3390/rs14041034."
INSERT: "C. R. Harris, K. J. Millman, S. J. van der Walt, R. Gommers, P. Virtanen, D. Cournapeau, E. Wieser, J. Taylor, S. Berg, N. J. Smith, R. Kern, M. Picus, S. Hoyer, M. H. van Kerkwijk, M. Brett, A. Haldane, J. Fernández del Río, M. Wiebe, P. Peterson, P. Gérard-Marchant, K. Sheppard, T. Reddy, W. Weckesser, H. Abbasi, C. Gohlke, T. E. Oliphant. Array programming with NumPy. Nature. Vol. 585, pg. 357–362, 2020, https://doi.org/10.1038/s41586-020-2649-2."

## P70
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "J. D. Hunter. Matplotlib: A 2D graphics environment. Computing in Science & Engineering. Vol. 9, pg. 90–95, 2007, https://doi.org/10.1109/MCSE.2007.55."
INSERT: "T. A. Worthington, P. S. E. zu Ermgassen, D. A. Friess, K. W. Krauss, C. E. Lovelock, J. Thorley, R. Tingey, C. D. Woodroffe, P. Bunting, N. Cormier, D. Lagomasino, R. Lucas, N. J. Murray, W. J. Sutherland, M. Spalding. A global biophysical typology of mangroves and its relevance for ecosystem structure and deforestation. Scientific Reports. Vol. 10, pg. 14652, 2020, https://doi.org/10.1038/s41598-020-71194-5."

## P71
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "lding. A global biophysical typology of mangroves and its relevance for ecosystem structure and deforestation. Scientific Reports. Vol. 10, pg. 14652, 2020, https://doi.org/10.1038/s41598-020-71194-5."
INSERT: "K. A. C. Gasparini, C. H. L. Silva Junior, Y. E. Shimabukuro, E. Arai, L. E. O. C. e Aragão, C. A. Silva, P. L. Marshall. Determining a threshold to delimit the Amazonian forests from the Tree Canopy Cover 2000 GFC data. Sensors. Vol. 19, pg. 5020, 2019, https://doi.org/10.3390/s19225020."

## P72
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "ão, C. A. Silva, P. L. Marshall. Determining a threshold to delimit the Amazonian forests from the Tree Canopy Cover 2000 GFC data. Sensors. Vol. 19, pg. 5020, 2019, https://doi.org/10.3390/s19225020."
INSERT: "A. Ghorbanian, S. Ahmadi, M. Amani, A. Mohammadzadeh, S. Jamali. Mangrove ecosystem mapping using Sentinel-1 and Sentinel-2 satellite images and random forest algorithm in Google Earth Engine. Remote Sensing. Vol. 13, pg. 2565, 2021, https://doi.org/10.3390/rs13132565."

## P73
OP: INSERT_AFTER_PARAGRAPH
PARAGRAPH_ENDS_WITH: "rove ecosystem mapping using Sentinel-1 and Sentinel-2 satellite images and random forest algorithm in Google Earth Engine. Remote Sensing. Vol. 13, pg. 2565, 2021, https://doi.org/10.3390/rs13132565."
INSERT: "N. J. Murray, T. A. Worthington, P. Bunting, S. Duce, V. Hagger, C. E. Lovelock, R. Lucas, M. I. Saunders, M. Sheaves, M. Spalding, N. J. Waltham, M. B. Lyons. High-resolution mapping of losses and gains of Earth's tidal wetlands. Science. Vol. 376, pg. 744–749, 2022, https://doi.org/10.1126/science.abm9583."
