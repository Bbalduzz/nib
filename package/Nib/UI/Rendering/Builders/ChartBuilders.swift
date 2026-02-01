import SwiftUI
import Charts

// MARK: - Chart View Builder

extension DynamicView {
    @ViewBuilder
    func buildChart() -> some View {
        let _ = debugPrint("[buildChart] chartData: \(String(describing: node.props.chartData)), children: \(String(describing: node.children?.count))")
        if let chartData = node.props.chartData {
            NibChartView(
                chartData: chartData,
                marks: node.children ?? [],
                xAxisConfig: node.props.xAxis,
                yAxisConfig: node.props.yAxis,
                legendConfig: node.props.legend,
                chartBackground: node.props.chartBackground,
                plotBackground: node.props.plotBackground,
                onEvent: onEvent
            )
        } else {
            Text("Chart: No data")
        }
    }
}

// MARK: - Chart Container View

struct NibChartView: View {
    let chartData: ViewNode.ChartData
    let marks: [ViewNode]
    let xAxisConfig: ViewNode.ChartAxisConfig?
    let yAxisConfig: ViewNode.ChartAxisConfig?
    let legendConfig: ViewNode.ChartLegendConfig?
    let chartBackground: String?
    let plotBackground: String?
    let onEvent: (String, String) -> Void

    // Parsed columns from JSON
    private var columns: [String: [Any]] {
        chartData.parseColumns()
    }

    // MARK: - Gradient Helpers

    /// Build gradient from PlottableField
    private func gradientFromField(_ field: ViewNode.PlottableField) -> Gradient {
        if let colors = field.colors {
            let swiftColors = colors.map { Color(nibColor: $0) }
            return Gradient(colors: swiftColors)
        }
        return Gradient(colors: [.clear])
    }

    /// Convert [x, y] array to UnitPoint
    private func unitPointFromField(_ array: [Double]?, default defaultPoint: UnitPoint) -> UnitPoint {
        guard let arr = array, arr.count >= 2 else { return defaultPoint }
        return UnitPoint(x: arr[0], y: arr[1])
    }

    var body: some View {
        let cols = columns
        let _ = debugPrint("[Chart] rowCount: \(chartData.rowCount), marks: \(marks.count), columns: \(cols.keys)")
        Chart {
            ForEach(0..<chartData.rowCount, id: \.self) { rowIndex in
                ForEach(marks) { markNode in
                    buildMarkContent(for: markNode, at: rowIndex, columns: cols)
                }
            }
        }
        .nibChartXAxis(xAxisConfig)
        .nibChartYAxis(yAxisConfig)
        .nibChartLegend(legendConfig)
        .nibChartBackground(chartBackground)
        .nibPlotBackground(plotBackground)
    }

    @ChartContentBuilder
    private func buildMarkContent(for node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        switch node.type {
        case .lineMark:
            buildLineMark(node: node, at: rowIndex, columns: columns)
        case .barMark:
            buildBarMark(node: node, at: rowIndex, columns: columns)
        case .areaMark:
            buildAreaMark(node: node, at: rowIndex, columns: columns)
        case .pointMark:
            buildPointMark(node: node, at: rowIndex, columns: columns)
        case .ruleMark:
            buildRuleMark(node: node, at: rowIndex, columns: columns)
        case .rectMark:
            buildRectMark(node: node, at: rowIndex, columns: columns)
        case .sectorMark:
            buildSectorMark(node: node, at: rowIndex, columns: columns)
        default:
            // Empty placeholder for non-mark types
            if false { LineMark(x: .value("", 0), y: .value("", 0)) }
        }
    }

    // MARK: - LineMark

    @ChartContentBuilder
    private func buildLineMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let xField = node.props.x?.field,
           let yField = node.props.y?.field,
           let xValue = getStringValue(field: xField, at: rowIndex, columns: columns),
           let yValue = getNumericValue(field: yField, at: rowIndex, columns: columns) {

            let interpolation = node.props.interpolation ?? "linear"
            let lineWidth = node.props.lineWidth ?? 2.0

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                // With foreground style grouping
                LineMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .lineStyle(StrokeStyle(lineWidth: lineWidth))
                .interpolationMethod(interpolationMethod(interpolation))
            } else if let gradientType = node.props.foregroundStyle?.gradientType,
                      let style = node.props.foregroundStyle {
                // Gradient foreground style
                let grad = gradientFromField(style)
                switch gradientType {
                case "LinearGradient":
                    let start = unitPointFromField(style.startPoint, default: UnitPoint(x: 0.5, y: 0))
                    let end = unitPointFromField(style.endPoint, default: UnitPoint(x: 0.5, y: 1))
                    LineMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .foregroundStyle(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
                        .lineStyle(StrokeStyle(lineWidth: lineWidth))
                        .interpolationMethod(interpolationMethod(interpolation))
                case "RadialGradient":
                    let center = unitPointFromField(style.center, default: .center)
                    LineMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .foregroundStyle(RadialGradient(gradient: grad, center: center, startRadius: style.startRadius ?? 0, endRadius: style.endRadius ?? 100))
                        .lineStyle(StrokeStyle(lineWidth: lineWidth))
                        .interpolationMethod(interpolationMethod(interpolation))
                default:
                    LineMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .lineStyle(StrokeStyle(lineWidth: lineWidth))
                        .interpolationMethod(interpolationMethod(interpolation))
                }
            } else if let colorStr = node.props.foregroundStyle?.color {
                // Direct color
                LineMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(Color(nibColor: colorStr))
                .lineStyle(StrokeStyle(lineWidth: lineWidth))
                .interpolationMethod(interpolationMethod(interpolation))
            } else {
                // Without foreground style
                LineMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .lineStyle(StrokeStyle(lineWidth: lineWidth))
                .interpolationMethod(interpolationMethod(interpolation))
            }
        }
    }

    // MARK: - BarMark

    @ChartContentBuilder
    private func buildBarMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let xField = node.props.x?.field,
           let yField = node.props.y?.field,
           let xValue = getStringValue(field: xField, at: rowIndex, columns: columns),
           let yValue = getNumericValue(field: yField, at: rowIndex, columns: columns) {

            let cornerRadius = node.props.cornerRadius ?? 0

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                BarMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .cornerRadius(cornerRadius)
            } else if let colorStr = node.props.foregroundStyle?.color {
                BarMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(Color(nibColor: colorStr))
                .cornerRadius(cornerRadius)
            } else {
                BarMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .cornerRadius(cornerRadius)
            }
        }
    }

    // MARK: - AreaMark

    @ChartContentBuilder
    private func buildAreaMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let xField = node.props.x?.field,
           let yField = node.props.y?.field,
           let xValue = getStringValue(field: xField, at: rowIndex, columns: columns),
           let yValue = getNumericValue(field: yField, at: rowIndex, columns: columns) {

            let interpolation = node.props.interpolation ?? "linear"
            let opacity = node.props.opacity ?? 1.0

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                AreaMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .interpolationMethod(interpolationMethod(interpolation))
                .opacity(opacity)
            } else if let gradientType = node.props.foregroundStyle?.gradientType,
                      let style = node.props.foregroundStyle {
                // Gradient foreground style
                let grad = gradientFromField(style)
                switch gradientType {
                case "LinearGradient":
                    let start = unitPointFromField(style.startPoint, default: UnitPoint(x: 0.5, y: 0))
                    let end = unitPointFromField(style.endPoint, default: UnitPoint(x: 0.5, y: 1))
                    AreaMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .foregroundStyle(LinearGradient(gradient: grad, startPoint: start, endPoint: end))
                        .interpolationMethod(interpolationMethod(interpolation))
                        .opacity(opacity)
                case "RadialGradient":
                    let center = unitPointFromField(style.center, default: .center)
                    AreaMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .foregroundStyle(RadialGradient(gradient: grad, center: center, startRadius: style.startRadius ?? 0, endRadius: style.endRadius ?? 100))
                        .interpolationMethod(interpolationMethod(interpolation))
                        .opacity(opacity)
                case "AngularGradient":
                    let center = unitPointFromField(style.center, default: .center)
                    AreaMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .foregroundStyle(AngularGradient(gradient: grad, center: center, startAngle: .degrees(style.startAngle ?? 0), endAngle: .degrees(style.endAngle ?? 360)))
                        .interpolationMethod(interpolationMethod(interpolation))
                        .opacity(opacity)
                default:
                    AreaMark(x: .value(xField, xValue), y: .value(yField, yValue))
                        .interpolationMethod(interpolationMethod(interpolation))
                        .opacity(opacity)
                }
            } else if let colorStr = node.props.foregroundStyle?.color {
                AreaMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(Color(nibColor: colorStr))
                .interpolationMethod(interpolationMethod(interpolation))
                .opacity(opacity)
            } else {
                AreaMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .interpolationMethod(interpolationMethod(interpolation))
                .opacity(opacity)
            }
        }
    }

    // MARK: - PointMark

    @ChartContentBuilder
    private func buildPointMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let xField = node.props.x?.field,
           let yField = node.props.y?.field,
           let xValue = getStringValue(field: xField, at: rowIndex, columns: columns),
           let yValue = getNumericValue(field: yField, at: rowIndex, columns: columns) {

            let symbolSize = node.props.symbolSize ?? 100

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                PointMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .symbolSize(symbolSize)
            } else {
                PointMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .symbolSize(symbolSize)
            }
        }
    }

    // MARK: - RuleMark

    @ChartContentBuilder
    private func buildRuleMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        // Horizontal rule (y value)
        if let yField = node.props.y,
           let yValue = getPlottableFieldNumericValue(field: yField, at: rowIndex, columns: columns) {
            RuleMark(y: .value(yField.field ?? "y", yValue))
                .lineStyle(StrokeStyle(lineWidth: node.props.lineWidth ?? 1))
        }
        // Vertical rule (x value)
        else if let xField = node.props.x,
                let xValue = getPlottableFieldStringValue(field: xField, at: rowIndex, columns: columns) {
            RuleMark(x: .value(xField.field ?? "x", xValue))
                .lineStyle(StrokeStyle(lineWidth: node.props.lineWidth ?? 1))
        }
    }

    // MARK: - RectMark

    @ChartContentBuilder
    private func buildRectMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let xField = node.props.x?.field,
           let yField = node.props.y?.field,
           let xValue = getStringValue(field: xField, at: rowIndex, columns: columns),
           let yValue = getNumericValue(field: yField, at: rowIndex, columns: columns) {

            let cornerRadius = node.props.cornerRadius ?? 0

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                RectangleMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .cornerRadius(cornerRadius)
            } else {
                RectangleMark(
                    x: .value(xField, xValue),
                    y: .value(yField, yValue)
                )
                .cornerRadius(cornerRadius)
            }
        }
    }

    // MARK: - SectorMark

    @ChartContentBuilder
    private func buildSectorMark(node: ViewNode, at rowIndex: Int, columns: [String: [Any]]) -> some ChartContent {
        if let angleField = node.props.angle?.field,
           let angleValue = getNumericValue(field: angleField, at: rowIndex, columns: columns) {

            let innerRadius = node.props.innerRadius ?? 0
            let outerRadius = node.props.outerRadius ?? 1.0
            let cornerRadius = node.props.cornerRadius ?? 0

            if let styleField = node.props.foregroundStyle?.field,
               let styleValue = getStringValue(field: styleField, at: rowIndex, columns: columns) {
                SectorMark(
                    angle: .value(angleField, angleValue),
                    innerRadius: .ratio(innerRadius),
                    outerRadius: .ratio(outerRadius)
                )
                .foregroundStyle(by: .value(styleField, styleValue))
                .cornerRadius(cornerRadius)
            } else {
                SectorMark(
                    angle: .value(angleField, angleValue),
                    innerRadius: .ratio(innerRadius),
                    outerRadius: .ratio(outerRadius)
                )
                .cornerRadius(cornerRadius)
            }
        }
    }

    // MARK: - Helpers

    private func getStringValue(field: String, at index: Int, columns: [String: [Any]]) -> String? {
        guard let column = columns[field], index < column.count else { return nil }
        let value = column[index]
        if let str = value as? String {
            return str
        }
        return String(describing: value)
    }

    private func getNumericValue(field: String, at index: Int, columns: [String: [Any]]) -> Double? {
        guard let column = columns[field], index < column.count else { return nil }
        let value = column[index]
        if let num = value as? Double {
            return num
        }
        if let num = value as? Int {
            return Double(num)
        }
        if let str = value as? String {
            return Double(str)
        }
        return nil
    }

    private func getPlottableFieldNumericValue(field: ViewNode.PlottableField, at index: Int, columns: [String: [Any]]) -> Double? {
        // Static value takes precedence
        if let fieldName = field.field {
            return getNumericValue(field: fieldName, at: index, columns: columns)
        }
        return nil
    }

    private func getPlottableFieldStringValue(field: ViewNode.PlottableField, at index: Int, columns: [String: [Any]]) -> String? {
        if let fieldName = field.field {
            return getStringValue(field: fieldName, at: index, columns: columns)
        }
        return nil
    }

    private func interpolationMethod(_ method: String) -> InterpolationMethod {
        switch method {
        case "monotone": return .monotone
        case "catmullRom": return .catmullRom
        case "cardinal": return .cardinal
        case "stepStart": return .stepStart
        case "stepCenter": return .stepCenter
        case "stepEnd": return .stepEnd
        default: return .linear
        }
    }
}

// MARK: - Chart Axis Modifiers

extension View {
    @ViewBuilder
    func nibChartXAxis(_ config: ViewNode.ChartAxisConfig?) -> some View {
        if let config = config {
            if config.hidden == true {
                self.chartXAxis(.hidden)
            } else {
                self.chartXAxis {
                    AxisMarks { _ in
                        if config.gridLines == true {
                            AxisGridLine()
                                .foregroundStyle(config.gridColor != nil ? Color(nibColor: config.gridColor!) : Color.gray.opacity(0.3))
                        }
                        AxisValueLabel()
                            .foregroundStyle(config.labelColor != nil ? Color(nibColor: config.labelColor!) : Color.primary)
                    }
                }
                .chartXAxisLabel(config.label ?? "")
            }
        } else {
            self
        }
    }

    @ViewBuilder
    func nibChartYAxis(_ config: ViewNode.ChartAxisConfig?) -> some View {
        if let config = config {
            if config.hidden == true {
                self.chartYAxis(.hidden)
            } else {
                self.chartYAxis {
                    AxisMarks { _ in
                        if config.gridLines == true {
                            AxisGridLine()
                                .foregroundStyle(config.gridColor != nil ? Color(nibColor: config.gridColor!) : Color.gray.opacity(0.3))
                        }
                        AxisValueLabel()
                            .foregroundStyle(config.labelColor != nil ? Color(nibColor: config.labelColor!) : Color.primary)
                    }
                }
                .chartYAxisLabel(config.label ?? "")
            }
        } else {
            self
        }
    }

    @ViewBuilder
    func nibChartLegend(_ config: ViewNode.ChartLegendConfig?) -> some View {
        if let config = config {
            if config.hidden == true {
                self.chartLegend(.hidden)
            } else {
                self.chartLegend(position: nibLegendPosition(config.position))
            }
        } else {
            self
        }
    }

    private func nibLegendPosition(_ position: String?) -> AnnotationPosition {
        switch position {
        case "top": return .top
        case "bottom": return .bottom
        case "leading": return .leading
        case "trailing": return .trailing
        default: return .automatic
        }
    }

    @ViewBuilder
    func nibChartBackground(_ color: String?) -> some View {
        if let colorStr = color {
            self.chartBackground { _ in
                Color(nibColor: colorStr)
            }
        } else {
            self
        }
    }

    @ViewBuilder
    func nibPlotBackground(_ color: String?) -> some View {
        if let colorStr = color {
            self.chartPlotStyle { plotArea in
                plotArea.background(Color(nibColor: colorStr))
            }
        } else {
            self
        }
    }
}
