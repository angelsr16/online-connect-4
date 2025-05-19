import { Component, EventEmitter, Input, Output } from '@angular/core';
import Konva from 'konva';
import { Game } from '../../../core/models/db/Game';
import { Circle } from 'konva/lib/shapes/Circle';
import { LocalGame } from '../../../core/models/LocalGame';

@Component({
  selector: 'app-local-game-board',
  imports: [],
  templateUrl: './local-game-board.component.html',
  styleUrl: './local-game-board.component.scss',
})
export class LocalGameBoardComponent {
  @Input() gameData!: LocalGame;
  @Output() onGameClick: EventEmitter<number> = new EventEmitter();

  private stage!: Konva.Stage;
  private layer!: Konva.Layer;
  private cellSize: number = 0;
  private rows: number = 6;
  private cols: number = 7;

  hoverCircle!: Circle;

  constructor() {}

  ngAfterViewInit(): void {
    this.initKonva();
    window.addEventListener('resize', () => {
      this.stage.destroy();
      this.initKonva();
    });
  }

  private initKonva() {
    const container = document.getElementById('board-container');
    if (!container || !this.gameData) return;

    const rect = container.getBoundingClientRect();
    const containerWidth = rect.width;
    const containerHeight = rect.height;

    const cellWidth = (containerWidth / this.cols) * 0.75;
    const cellHeight = (containerHeight / this.rows) * 0.75;

    this.cellSize = Math.floor(Math.min(cellWidth, cellHeight));
    const width = this.cellSize * this.cols;
    const height = this.cellSize * this.rows;

    this.stage = new Konva.Stage({
      container: 'container',
      width,
      height,
    });

    this.layer = new Konva.Layer();
    this.stage.add(this.layer);

    this.hoverCircle = new Konva.Circle({
      x: 0 * this.cellSize + this.cellSize / 2,
      y: 5 * this.cellSize + this.cellSize / 2,
      radius: this.cellSize / 2.5,
      fill: this.gameData.current_turn === 1 ? '#ff6767' : '#f9ff9d',
    });

    this.stage.on('mousemove', () => {
      this.positionHoverCircle();
    });

    this.stage.on('click', () => {
      const pos = this.stage.getPointerPosition();
      if (!pos) return;
      const column = Math.floor((pos.x / width) * this.cols);
      this.onGameClick.emit(column);
    });

    this.drawGrid();
    this.layer.add(this.hoverCircle);
  }

  positionHoverCircle() {
    const pos = this.stage.getPointerPosition();
    if (!pos) return;
    const column = Math.floor(
      (pos.x / (this.cellSize * this.cols)) * this.cols
    );

    var rowPosCirclePreview = this.getCirclePreview(column);

    this.hoverCircle.position({
      x: column * this.cellSize + this.cellSize / 2,
      y: rowPosCirclePreview * this.cellSize + this.cellSize / 2,
    });

    this.layer.batchDraw();
  }

  updateGame(gameData: LocalGame) {
    this.gameData = gameData;
    this.drawGrid();

    if (this.gameData.isGameOver) {
      this.hoverCircle.destroy();
    } else {
      this.positionHoverCircle();
    }
  }

  private drawGrid() {
    this.layer.removeChildren();

    const grid = new Konva.Rect({
      x: 0,
      y: 0,
      width: this.cellSize * this.cols,
      height: this.cellSize * this.rows,
      fill: 'blue',
      stroke: '#000000',
      strokeWidth: 2,
      cornerRadius: 25,
    });
    this.layer.add(grid);

    this.gameData.game_state.forEach((row, rowIndex) => {
      row.forEach((col, colIndex) => {
        var color = '#fff';
        switch (col) {
          case 1:
            color = 'red';
            break;
          case 2:
            color = 'yellow';
            break;
        }

        this.drawCell(rowIndex, colIndex, color);
      });
    });

    this.hoverCircle.fill(
      this.gameData.current_turn === 1 ? '#ff6767' : '#f9ff9d'
    );
    this.layer.add(this.hoverCircle);

    this.layer.draw();
  }

  private drawCell(row: number, col: number, color: string) {
    const circle = new Konva.Circle({
      x: col * this.cellSize + this.cellSize / 2,
      y: row * this.cellSize + this.cellSize / 2,
      radius: this.cellSize / 2.5,
      fill: color,
      stroke: '#000000',
      strokeWidth: 2,
    });

    this.layer.add(circle);
  }

  getCirclePreview(columnIndex: number): number {
    for (let row = this.gameData.game_state.length - 1; row >= 0; row--) {
      const cell = this.gameData.game_state[row][columnIndex];
      if (cell === 0) {
        return row;
      }
    }
    return -1;
  }

  onLeftClick() {}

  onRightClick() {}
}
