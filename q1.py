import sys
import time
import copy
import random
from collections import defaultdict #ファイルの入れ込みのためのライブリー


def bench_demo():
    """
    ベンチマークデモ：
    - ランダムな疎グラフを生成
    - ベース版と高速版を同条件で実行し、時間を比較表示
    """
    # 毎回同じグラフになるよう固定
    random.seed(42)

    M = 20_0000            # ニューロン数
    edges_per_neuron = 3  # 1ニューロンあたり出次数
    N = 1500               # ステップ数

    # 疎なランダム接続を作る（1始まり）
    connections = []
    for u in range(1, M + 1):
        for _ in range(edges_per_neuron):
            v = random.randint(1, M)
            w = random.random()
            connections.append((u, v, w))
    
    # 初期状態：1% だけ活性、しきい値は0.5固定（比較目的なのでシンプルに）
    neurons = [{"id": i+1,
                "state": 1 if random.random() < 0.01 else 0,
                "threshold": 0.5}
               for i in range(M)]
    
    print(f"[Bench] M={M}, edges={M*edges_per_neuron}, steps={N}")
    
    # ベースライン
    t0 = time.time()
    simulate_N(copy.deepcopy(neurons), connections, N)
    t1 = time.time() - t0
    print(f"baseline: {t1:.3f}s")

    # 高速版
    t0 = time.time()
    simulate_fast(copy.deepcopy(neurons), connections, N)
    t2 = time.time() - t0
    print(f"fast    : {t2:.3f}s")



def verify_stdin():
    """
    検証モード：
    - 標準入力から1ケースだけ読み取り
    - ベース版(simulate_N)と高速版(simulate_fast)を同じ入力で実行
    - 出力・一致判定・実行時間を表示
    """

    # 入力は一度だけ読む（同じデータを両方に使う）
    neurons, connections, N = _read_stdin_case()

    # ディープコピーして、双方に同じ初期状態を渡す
    neurons_base = copy.deepcopy(neurons)
    neurons_fast = copy.deepcopy(neurons)

    # ベースライン
    t0 = time.time()
    base_out = simulate_N(neurons_base, connections, N, debug_every=None)
    t1 = time.time() - t0

    # 高速版
    t0 = time.time()
    fast_out = simulate_fast(neurons_fast, connections, N, debug_every=None)
    t2 = time.time() - t0

    # 表示
    print("BASE :", *base_out)
    print("FAST :", *fast_out)
    print("MATCH:", base_out == fast_out)
    print(f"time  baseline={t1:.6f}s  fast={t2:.6f}s")

def simulate_fast(neurons, connections, N, debug_every=None):
    """
    高速版シミュレータ:
    - まず一度だけ隣接リスト out_edges を作成
    - 各ステップで step_fast を使って状態を更新
    """
    M = len(neurons)
    out_edges = build_out_edges(M, connections)

    for t in range(1, N + 1):
        step_fast(neurons, out_edges)
        if debug_every is not None and t % debug_every == 0:
            print(f"STEP {t:>4}: {[n['state'] for n in neurons]}")

    return [n["state"] for n in neurons]

def step_fast(neurons, out_edges):
    """
    高速版: 活性ニューロン u の out_edges[u] だけを辿って受信を加算する
    - out_edges は build_out_edges(M, connections) で作る (0始まりの (v, w) リスト)
    """

    M = len(neurons)
    received = [0.0] * M

    # 1. 受信フェーズ
    for u, nu in enumerate(neurons):
        if nu["state"] == 1:
            for v, w in out_edges[u]:
                received[v] += w


    # 2. 状態更新フェーズの保存
    new_states = [0] * M
    for i in range(M):
        if received[i] >= neurons[i]["threshold"]:
            new_states[i] = 1
        else:
            new_states[i] = 0


    # 3. 状態更新の本フェーズ
    for i in range(M):
        neurons[i]["state"] = new_states[i]

    
    return [n["state"] for n in neurons]

def build_out_edges(M, connections):
    """
    各ニューロンから出る接続(隣接リスト)を作成する関数
    - out_edges[u] はニューロン u から出る全ての接続先 (v, w) のリスト
    - 同じ接続先が複数ある場合は重みを合計する
    """
    # 各ニューロンごとに {接続先: 重み} を管理する辞書を用意
    out_edges = [defaultdict(float) for _ in range(M)]

    # 接続情報を読み込んで隣接リストを作成
    for a, b, w in connections:
        u = a - 1 # 入力は1始まりなので0始まりに変換
        v = b - 1
        out_edges[u][v] += w # 同じ接続先があれば重みを加算
    
    return [list(edges.items()) for edges in out_edges]


def solve_stdin_fast():
    """
    ジャッジ(高速版)：標準入力→高速シミュレータ→最終状態を出力
    """

    # 1. ニューロン配列を作成
    neurons, connections, N = _read_stdin_case()

    # 2. 高速版で N ステップ実行
    final_states = simulate_fast(neurons, connections, N, debug_every=None)

    # 3. 出力（空白区切り）
    print(*final_states)


def solve_stdin():
    """
    ジャッジモード： 問題文で指定された形式で標準入力からデータを読み込み、最終的なニューロンの状態を出力する
    """  

    #1. 辞書形式でニューロンを生成
    neurons, connections, N = _read_stdin_case()

    #2. Nステップの実行
    final_states = simulate_N(neurons, connections, N, debug_every=None)

    #3.出力させる（*は空白を入れる）
    print(*final_states)
    

def _read_stdin_case():
    """
    標準入力から 1 ケース分を読み取り、(neurons, connections, N) を返す内部関数
    """
    input = sys.stdin.readline

    # 1. M（ニューロン数）
    M = int(input().strip())

    # 2. 初期状態 s(1..M)
    s = list(map(int, input().split()))

    # 3. しきい値 X(1..M)
    X = list(map(float, input().split()))

    # 4. ステップ数 N
    N = int(input().strip())

    # 5. 接続 (a b w) を 'E' まで読み込む
    connections = []
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if line == 'E':
            break
        a, b, w = line.split()
        connections.append((int(a), int(b), float(w)))


    # ニューロン配列（辞書のリスト）を作成
    neurons = [{"id": i+1, "state": s[i], "threshold": X[i]} for i in range(M)]
    return neurons, connections, N

def steps(neurons, connections, debug=False):
    """
    neurons: ニューロンのリスト（辞書形式）
    connections: 接続リスト (a, b, w)
    """
    M = len(neurons) #ニューロン数

    #1. 受信信号の合計の初期化
    received = [0.0] * M

    #2. 信号の送信
    for a, b, w in connections:
        #aニューロンが活性なら信号を送る
        if neurons[a-1]["state"] == 1:
            received[b-1] += w
    
    #       確認のためのデバッグ
    if debug:
        print("RECEIVED:", [round(x, 3) for x in received])
    


    #3. 状態更新フェーズの保存
    new_states = [0] *M
    for i in range(M):
        if received[i] >= neurons[i]["threshold"]:
            new_states[i]= 1
        else:
            new_states[i]= 0
    
    #4. 状態更新の本フェーズ
    for i in range(M):
        neurons[i]["state"] = new_states[i]


    #新状態を返す
    return [n["state"] for n in neurons]

def simulate_N(neurons, connections, N, debug_every=None):
    """
    N 回ステップを進め、最終状態 (0/1 のリスト) を返す関数
    - neurons: 辞書のリスト（"state", "threshold" など）
    - connections: (a, b, w) のタプルのリスト
    - N: ステップ数
    - debug_every: 例) 10 を指定すると 10 ステップごとに状態を表示。None なら表示なし
    最終的に、リストとして返す
    """
    for t in range(1, N + 1):

        steps(neurons, connections, debug=False)
        if debug_every is not None and t % debug_every == 0:
            print(f"STEP {t:>4}: {[n['state'] for n in neurons]}")

    return [n["state"] for n in neurons]


#ニューロンの状態（1･0）としきい値
neurons = [
    {"id" : 1, "state":1, "threshold": 0.5},
    {"id" : 2, "state":1, "threshold": 0.1},
    {"id" : 3, "state":1, "threshold": 0.6},
    {"id" : 4, "state":1, "threshold": 0.5},
    {"id" : 5, "state":0, "threshold": 0.4},
    {"id" : 6, "state":1, "threshold": 0.8},
    {"id" : 7, "state":1, "threshold": 0.2},
    {"id" : 8, "state":1, "threshold": 0.2},
    {"id" : 9, "state":0, "threshold": 0.4},
]

#ニューロンAからBまでの信号の強さW
connections = [
    (4, 3, 0.8),
    (9, 6, 0.6),
    (8, 3, 0.4),
    (7, 9, 0.6),
    (4, 3, 1.0),
    (2, 6, 0.8),
    (1, 4, 0.8),
    (2, 1, 0.5),
    (4, 4, 0.1),
    (5, 5, 0.8),
    (3, 7, 0.5),
    (9, 8, 0.3),
    (8, 2, 0.6),
]



def main():
    import sys
    # モード
    #   デモ：python3 q1.py
    #   ジャッジ(ベース)：python3 q1.py --stdin
    #   ジャッジ(高速)   ：python3 q1.py --stdin-fast
    #   検証              ：python3 q1.py --verify-stdin < input.txt
    #   ベンチ            ：python3 q1.py --bench-demo

    if len(sys.argv) > 1:
        if sys.argv[1] == "--stdin":
            solve_stdin()
        elif sys.argv[1] == "--stdin-fast":
            solve_stdin_fast()
        elif sys.argv[1] == "--verify-stdin":
            verify_stdin()
        elif sys.argv[1] == "--bench-demo":
            bench_demo()


        else:
            print("Unknown option:", sys.argv[1])
            print("Usage: python3 q1.py [--stdin | --stdin-fast | --verify-stdin | --bench-demo]")
    else:
        print("BEFORE:", [n["state"] for n in neurons])
        final_states = simulate_N(neurons, connections, N=100, debug_every=None)
        print("AFTER :", final_states)

if __name__ == "__main__":
    main()