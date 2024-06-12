import * as d3 from 'd3'
import { chain } from 'lodash'

export const useStatistics = () => {
  // TODO: transfer mostReviewed here
  // ensure functions added here pertain to stat calculations only

  /**
   * Parses the resulting list of movies and retrieves
   * the top five most reviewed films according to the database.
   * 
   * @param {Object} data 
   * @returns {Array<Object>}
   */
  function mostReviewed (data) {
    const reviewCount = chain(data)
      .filter(i => i?.review_count)
      .value()
    const sortedReviewCount = reviewCount.slice().sort((a, b) => d3.descending(a.review_count, b.review_count));
    const topFive = sortedReviewCount.slice(0,5)
    return topFive
  }

  /**
   * Parses the resulting list of movies and retrieves
   * the top five most viewed films.
   * 
   * @param {Object} data 
   * @returns {Array<Object>}
   */
  function mostViewed (data) {
    const viewCount = chain(data)
      .filter(i => i?.watch_count)
      .value()
    const sortedViewCount = viewCount.slice().sort((a, b) => d3.descending(a.watch_count, b.watch_count))
    const topFive = sortedViewCount.slice(0,5)
    return topFive
  }

  return {
    mostReviewed,
    mostViewed
  }
}