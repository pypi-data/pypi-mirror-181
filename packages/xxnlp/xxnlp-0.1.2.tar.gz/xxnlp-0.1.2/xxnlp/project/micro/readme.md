每一个句子都会得到如下结果:
{
    max_score: score, top_k_scores: [(seed, score), (seed, score), ...], query: 本句
}   # 类似于我们用knowledge去query每一个entity
然后把threshold(max-score) > 0.8的, 提取出来, 然后统计哪些query符合条件