import csv
import time
import os
from app.config.constants import ModelType, DistanceMetricType, BackendType, NormalizationType
from deepface import DeepFace
from concurrent.futures import ThreadPoolExecutor

image_input = './faces/72391682.jpg'
image_correct = './query/jorge.jpeg'
image_fail = './dnis/70543329.jpg'

progress_file = 'progress.txt'

def run_verify_wrapper(args):
    return run_verify(*args)

def run_verify(image1, image2, model, distance_metric, detector_backend, normalization):
    very = DeepFace.verify(
        image1,
        image2,
        model_name=model,
        distance_metric=distance_metric,
        detector_backend=detector_backend,
        normalization=normalization
    )
    return very['verified']

def test_combination(combination):
    model, distance, backend, normalization = combination
    average_time = []
    last_result1 = False
    last_result2 = False
    for _ in range(number_test):
        start = time.time()
        res1 = run_verify(image_input, image_correct, model, distance, backend, normalization)
        end = time.time()
        average_time.append(end - start)
        last_result1 = res1

        start = time.time()
        res2 = run_verify(image_input, image_fail, model, distance, backend, normalization)
        end = time.time()
        average_time.append(end - start)
        last_result2 = not res2

    average_time = sum(average_time) / len(average_time)
    return [model, distance, backend, normalization, average_time, last_result1, last_result2]

def testings():
    modelList = list(ModelType)
    distanceList = list(DistanceMetricType)
    backendList = list(BackendType)
    normalizationList = list(NormalizationType)

    combinations = [(model.value, distance.value, backend.value, normalization.value) for model in modelList
                                                               for distance in distanceList
                                                               for backend in backendList
                                                               for normalization in normalizationList]
    
    if os.path.exists(progress_file):
        with open(progress_file, 'r') as f:
            last_index = int(f.read().strip())
            combinations = combinations[last_index:]

    print(len(combinations))
    with open('results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Modelo', 'Distancia', 'Backend', 'Normalización', 'Tiempo promedio', 'Resultado1', 'Resultado2'])
        for i, combination in enumerate(combinations, start=1):
            result = test_combination(combination)
            writer.writerows([result])
            # Guardar el índice de la última combinación probada
            with open(progress_file, 'w') as f:
                f.write(str(i))

if __name__ == "__main__":
    number_test = 3
    testings()
